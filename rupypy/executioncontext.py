from pypy.rlib import jit

from rupypy.error import RubyError
from rupypy.frame import Frame


class IntegerWrapper(object):
    def __init__(self, value):
        self.value = value


class ExecutionContext(object):
    def __init__(self):
        self.topframeref = jit.vref_None
        self.last_instr_ref = None

    def enter(self, frame):
        frame.backref = self.topframeref
        if self.last_instr_ref is not None:
            frame.back_last_instr = self.last_instr_ref.value
            self.last_instr_ref = None
        self.topframeref = jit.virtual_ref(frame)

    def leave(self, frame, got_exception):
        frame_vref = self.topframeref
        self.topframeref = frame.backref
        if frame.escaped or got_exception:
            back = frame.backref()
            if back is not None:
                back.escaped = True
            frame_vref()
        jit.virtual_ref_finish(frame_vref, frame)

    def visit_frame(self, frame):
        return _VisitFrameContextManager(self, frame)

    def gettopframe(self):
        return self.topframeref()

    @jit.unroll_safe
    def gettoprubyframe(self):
        frame = self.gettopframe()
        while frame is not None and not isinstance(frame, Frame):
            frame = frame.backref()
        return frame


class _VisitFrameContextManager(object):
    def __init__(self, ec, frame):
        self.ec = ec
        self.frame = frame

    def __enter__(self):
        self.ec.enter(self.frame)

    def __exit__(self, exc_type, exc_value, tb):
        if exc_value is not None and isinstance(exc_value, RubyError):
            if exc_value.w_value.frame is None:
                exc_value.w_value.frame = self.frame

        self.ec.leave(self.frame, exc_value is not None)
