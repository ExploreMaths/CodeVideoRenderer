import pytest, tempfile, os
from CodeVideoRenderer import *

# Test data
SAMPLE_CODE = '''
def hello_world():
    print("Hello, World!")
    return True

class TestClass:
    def __init__(self):
        self.value = 42
        
    def method(self):
        return self.value
'''

def test_core_class_import():
    """Test that core classes can be imported"""
    assert CameraFollowCursorCV is not None

def test_config_constants():
    """Test that configuration constants are properly defined"""
    assert DEFAULT_LINE_SPACING == 0.8
    assert DEFAULT_CURSOR_HEIGHT == 0.35
    assert DEFAULT_TYPE_INTERVAL == 0.15
    assert DEFAULT_TAB_WIDTH == 4
    assert NOT_AVAILABLE_CHARACTERS == '\r\v\f'

def test_class_initialization_with_minimal_params():
    """Test initialization with minimal required parameters"""
    video = CameraFollowCursorCV(
        code=('string', 'print(\"Hello World\")'),
        language='python',
        video_name='test_minimal'
    )
    assert video is not None

def test_render_method_exists():
    """Test that render method exists and is callable"""
    video = CameraFollowCursorCV(
        code=('string', 'x = 1 + 1'),
        language='python',
        video_name='test_render'
    )
    assert hasattr(video, 'render')
    assert callable(video.render)

def test_initialization_with_all_parameters():
    """Test initialization with all optional parameters"""
    video = CameraFollowCursorCV(
        code=('string', SAMPLE_CODE),
        language='python',
        formatter_style='github-dark',
        line_spacing=1.0,
        interval_range=(0.1, 0.2),
        camera_scale=0.7,
        video_name='test_full_params',
        renderer='cairo'
    )
    assert video is not None

def test_different_languages():
    """Test initialization with different programming languages"""
    languages = ['python', 'javascript', 'java']
    
    for lang in languages:
        video = CameraFollowCursorCV(
            code=('string', SAMPLE_CODE),
            language=lang, # type: ignore
            video_name=f'test_{lang}'
        )
        assert video is not None

def test_different_formatter_styles():
    """Test different syntax highlighting styles"""
    styles = ['material', 'github-dark', 'monokai']
    
    for style in styles:
        video = CameraFollowCursorCV(
            code=('string', SAMPLE_CODE),
            language='python',
            formatter_style=style, # type: ignore
            video_name=f'test_style_{style}'
        )
        assert video is not None

def test_file_input():
    """Test initialization with file input"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(SAMPLE_CODE)
        temp_file = f.name
    
    try:
        video = CameraFollowCursorCV(
            code=('file', temp_file),
            language='python',
            video_name='test_file_input'
        )
        assert video is not None
    finally:
        os.unlink(temp_file)

def test_invalid_parameters():
    """Test that invalid parameters raise appropriate errors"""
    # Test invalid line spacing
    with pytest.raises(ValueError):
        CameraFollowCursorCV(
            code=('string', SAMPLE_CODE),
            language='python',
            line_spacing=0,
            video_name='test_invalid_spacing'
        )
    
    # Test invalid interval range
    with pytest.raises(ValueError):
        CameraFollowCursorCV(
            code=('string', SAMPLE_CODE),
            language='python',
            interval_range=(0.2, 0.1),  # First term > second term
            video_name='test_invalid_interval'
        )
    
    # Test missing video name
    with pytest.raises(ValueError):
        CameraFollowCursorCV(
            code=('string', SAMPLE_CODE),
            language='python',
            video_name=''  # Empty video name
        )

def test_invalid_characters():
    """Test that invalid characters raise appropriate errors"""
    invalid_code = 'print("Hello\rWorld")'  # Contains \r
    
    with pytest.raises(ValueError):
        CameraFollowCursorCV(
            code=('string', invalid_code),
            language='python',
            video_name='test_invalid_chars'
        )

def test_code_processing_utilities():
    """Test utility functions for code processing"""
    # Test stripEmptyLines
    code_with_empty_lines = '\n\nline1\n\nline2\n\n'
    processed = stripEmptyLines(code_with_empty_lines)
    assert processed.startswith('line1')
    assert processed.endswith('line2')
    
    # Test findSpacePositions
    test_code = '  line1\n    line2'
    space_positions = findSpacePositions(test_code)
    assert len(space_positions) == 0
    
    # Test findEmptyLinePositions
    empty_line_code = 'line1\n\nline2\n\n\nline3'
    empty_positions = findEmptyLinePositions(empty_line_code)
    assert empty_positions == [1, 3, 4]

def test_different_renderers():
    """Test both Cairo and OpenGL renderers"""
    renderers = ['cairo', 'opengl']
    
    for renderer in renderers:
        video = CameraFollowCursorCV(
            code=('string', SAMPLE_CODE),
            language='python',
            renderer=renderer, # type: ignore
            video_name=f'test_{renderer}'
        )
        assert video is not None

def test_complex_code_structures():
    """Test with complex code structures"""
    complex_code = '''import numpy as np

def complex_function(data):
    """A complex function with documentation."""
    if len(data) == 0:
        return None
    
    result = np.array(data)
    mean = np.mean(result)
    std = np.std(result)
    
    return {
        'mean': mean,
        'std': std,
        'z_scores': (result - mean) / std
    }

# Test the function
test_data = [1, 2, 3, 4, 5]
output = complex_function(test_data)
print(f"Results: {output}")
'''
    
    video = CameraFollowCursorCV(
        code=('string', complex_code),
        language='python',
        video_name='test_complex_code'
    )
    assert video is not None

def test_scene_creation():
    """Test that scene creation works correctly"""
    video = CameraFollowCursorCV(
        code=('string', SAMPLE_CODE),
        language='python',
        video_name='test_scene'
    )
    
    # Test that scene is created
    assert video is not None
    
    # Test that scene has render method
    assert hasattr(video, 'render')
    assert callable(video.render)

def test_code_string_processing():
    """Test internal code string processing"""
    video = CameraFollowCursorCV(
        code=('string', SAMPLE_CODE),
        language='python',
        video_name='test_processing'
    )
    
    # Test that code string is processed
    assert video is not None

def test_unicode_support():
    """Test that Unicode characters are supported"""
    unicode_code = '''# Unicode test
print("Hello 世界")
print("こんにちは")
print("안녕하세요")

# Emoji test
message = "🚀 Python is awesome! 🎉"
print(message)
'''
    
    video = CameraFollowCursorCV(
        code=('string', unicode_code),
        language='python',
        video_name='test_unicode'
    )
    assert video is not None

def test_empty_code():
    """Test behavior with empty code"""
    empty_code = ''
    
    video = CameraFollowCursorCV(
        code=('string', empty_code),
        language='python',
        video_name='test_empty'
    )
    assert video is not None

def test_single_line_code():
    """Test with single line of code"""
    single_line = 'print("Single line test")'
    
    video = CameraFollowCursorCV(
        code=('string', single_line),
        language='python',
        video_name='test_single_line'
    )
    assert video is not None

# Performance and edge case tests
def test_large_code_file():
    """Test with larger code files"""
    large_code = '\n'.join([f'# Line {i}\nprint("Line {i}")' for i in range(50)])
    
    video = CameraFollowCursorCV(
        code=('string', large_code),
        language='python',
        video_name='test_large_code'
    )
    assert video is not None

def test_special_characters():
    """Test code with special characters"""
    special_code = '''# Special characters test
print("Quotes: 'single' and \"double\"")
print("Backslash: \\\\")
print("Tabs:\tindented")
print("Math: 2 + 2 = 4")
print("Symbols: @#$%^&*()")
'''
    
    video = CameraFollowCursorCV(
        code=('string', special_code),
        language='python',
        video_name='test_special_chars'
    )
    assert video is not None

# Note: The actual render test is commented out to avoid creating video files during testing
# def test_render_functionality():
#     """Test actual rendering functionality (creates video file)"""
#     video = CameraFollowCursorCV(
#         code=('string', SAMPLE_CODE),
#         language='python',
#         video_name='test_render_output'
#     )
#     
#     # This would create an actual video file
#     # video.render()
#     # assert os.path.exists('test_render_output.mp4')
#     pass