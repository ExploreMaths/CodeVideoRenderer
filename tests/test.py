from CodeVideoRenderer import CameraFollowCursorCV

def test_core_class_import():
    """测试核心类能正常导入"""
    assert CameraFollowCursorCV is not None

def test_class_initialization_with_minimal_params():
    """测试使用最小必填参数初始化不崩溃"""
    video = CameraFollowCursorCV(
        code=('string', 'print("Hello World")'),
        language='python',
        video_name='test_minimal'
    )
    assert video is not None

def test_render_method_exists():
    """测试核心render方法存在"""
    video = CameraFollowCursorCV(
        code=('string', 'x = 1 + 1'),
        language='python',
        video_name='test_render'
    )
    assert hasattr(video, 'render')
    assert callable(video.render)

def test_add_text_overlay_method_exists():
    """测试添加文字叠加层的方法存在"""
    video = CameraFollowCursorCV(
        code=('string', 'a = 2'),
        language='python',
        video_name='test_overlay'
    )
    assert hasattr(video, 'add_text_overlay')
    assert callable(video.add_text_overlay)

def test_code_parameter_validation():
    """测试code参数格式验证（元组形式）"""
    # 测试正确的code格式
    valid_code = ('string', 'print("test")')
    video = CameraFollowCursorCV(
        code=valid_code,
        language='python',
        video_name='test_validation'
    )
    assert video.code == valid_code
