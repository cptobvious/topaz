from ..base import BaseTopazTest


class TestStructObject(BaseTopazTest):
    def no_test_length(self, space):
        w_res = space.execute("return Struct.new(:a, :b, :c).length")
        assert space.int_w(w_res) == 3

    def test_stuff_1(self, space):
        w_res = space.execute("return Struct.name")
        assert space.str_w(w_res) == "Struct"

    def test_stuff_2(self, space):
        w_res = space.execute("return Struct.class.name")
        assert space.str_w(w_res) == "Class"

    def test_stuff_3(self, space):
        with self.raises(space, "ArgumentError", "wrong number of arguments (0 for 1+)"):
            space.execute("Struct.new")

    def test_stuff_4(self, space):
        w_res = space.execute("return Struct.new(:foo).class.name")
        assert space.str_w(w_res) == "Class"

    def test_stuff_5(self, space):
        w_res = space.execute("return Struct.new(:foo).superclass.name")
        assert space.str_w(w_res) == "Struct"

    def test_stuff_6(self, space):
        with self.raises(space, "TypeError", "allocator undefined for Struct"):
            space.execute("Struct.allocate")

    def test_stuff_7(self, space):
        w_res = space.execute("return Struct.new(:foo)")
        print "res", w_res

    def test_stuff_8(self, space):
        w_res = space.execute("""
        x = Struct.new(:foo)
        y = x.new(4)
        return y.class
        """)
        print "res", w_res

    def test_stuff_9(self, space):
        w_res = space.execute("return Struct.new('Foo')")
        w_cls = space.w_struct.constants_w["Foo"]
        assert w_res is w_cls

    def test_stuff_10(self, space):
        w_res = space.execute("return Struct.new('Foo').class.name")
        assert space.str_w(w_res) == "Struct::Foo"

    def test_stuff_11(self, space):
        w_res = space.execute("return Struct.new(:a).new.a")
        assert w_res == space.w_nil
