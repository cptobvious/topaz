from rupypy.module import ClassDef
from rupypy.modules.enumerable import Enumerable
from rupypy.objects.objectobject import W_Object
from rupypy.objects.intobject import W_FixnumObject


class W_RangeObject(W_Object):
    classdef = ClassDef("Range", W_Object.classdef)
    classdef.include_module(Enumerable)

    def __init__(self, space, w_start, w_end, exclusive):
        W_Object.__init__(self, space)

        if not isinstance(w_start, W_FixnumObject):
            raise NotImplementedError(type(w_start))

        if not isinstance(w_end, W_FixnumObject):
            raise NotImplementedError(type(w_end))

        self.w_start = w_start
        self.w_end = w_end
        self.exclusive = exclusive

    # TODO:
    # This shouldn't take args_w, it should take start, stop, inclusive arguments, and use default args for it. Also, this should probably implement allocate, instead of new.
    #@classdef.singleton_method("new")
    #def method_new(self, space, args_w):
    #    if len(args_w) < 3:
    #        return W_RangeObject(space, args_w[0], args_w[1], False)
    #    else:
    #        return W_RangeObject(space, args_w[0], args_w[1], space.bool_w(args_w[2]))

    @classdef.method("begin")
    def method_begin(self, space):
        return self.w_start

    @classdef.method("end")
    def method_end(self, space):
        return self.w_end

    @classdef.method("exclude_end?")
    def method_exclude_end(self, space):
        return space.newbool(self.exclusive)

    classdef.app_method("""
    def ==(other)
        if other.instance_of? Range
            if self.begin == other.begin && self.end == other.end && 
                if self.exclude_end? == other.exclude_end?
                    return true
                end
            end
        end
        false
    end

    def ===(other)
        include? other
    end

    def member?(other)
        include? other
    end

    def include?(other)
        if other.is_a? Fixnum
            return cover? other
        end
        self.each do |i|
            return true if i == other
        end
        false
    end

    def cover?(other)
        if self.begin <= other
            if self.exclude_end?
                if other < self.end
                    return true
                end
            else
                if other <= self.end
                    return true
                end
            end
        end
        false
    end
    
    def each
        i = self.begin
        lim = self.end
        if !self.exclude_end?
            lim = lim.succ
        end
        while i < lim
            yield i
            i = i.succ
        end
    end

    def to_a
        x = []
        self.each do |elem|
            x << elem
        end
        x
    end
    """)
