from ..base import BaseRuPyPyTest


class TestStringObject(BaseRuPyPyTest):
    def test_lshift(self, space):
        w_res = space.execute('return "abc" << "def" << "ghi"')
        assert self.unwrap(space, w_res) == "abcdefghi"

    def test_plus(self, space):
        w_res = space.execute('return "abc" + "def" + "ghi"')
        assert self.unwrap(space, w_res) == "abcdefghi"

    def test_to_s(self, space):
        w_res = space.execute('return "ABC".to_s')
        assert self.unwrap(space, w_res) == "ABC"

    def test_length(self, space):
        w_res = space.execute("return 'ABC'.length")
        assert self.unwrap(space, w_res) == 3

    def test_comparator_lt(self, space):
        w_res = space.execute("return 'a' <=> 'b'")
        assert self.unwrap(space, w_res) == -1

    def test_comparator_eq(self, space):
        w_res = space.execute("return 'a' <=> 'a'")
        assert self.unwrap(space, w_res) == 0

    def test_comparator_gt(self, space):
        w_res = space.execute("return 'b' <=> 'a'")
        assert self.unwrap(space, w_res) == 1

    def test_hash(self, space):
        w_res = space.execute("""
        return ['abc'.hash, ('a' << 'b' << 'c').hash]
        """)
        h1, h2 = self.unwrap(space, w_res)
        assert h1 == h2

    def test_to_sym(self, space):
        w_res = space.execute("return 'abc'.to_sym")
        assert space.symbol_w(w_res) == "abc"

    def test_clear(self, space):
        w_res = space.execute("""
        a = 'hi'
        b = a
        a.clear
        return [a, b]
        """)
        assert self.unwrap(space, w_res) == ["", ""]

        w_res = space.execute("return ('a' << 'b').clear")
        assert self.unwrap(space, w_res) == ""

    def test_subscript(self, space):
        w_res = space.execute("return 'abcdefg'[1]")
        assert self.unwrap(space, w_res) == "b"

    def test_range_inclusive(self, space):
        w_res = space.execute("return 'abcdefg'[1..2]")
        assert self.unwrap(space, w_res) == "bc"

    def test_range_exclusive(self, space):
        w_res = space.execute("return 'abcdefg'[1...3]")
        assert self.unwrap(space, w_res) == "bc"

    def test_edge_indices(self, space):
        w_res = space.execute("return 'hello'[5]")
        assert self.unwrap(space, w_res) is None

        w_res = space.execute("return 'hello'[-2]")
        assert self.unwrap(space, w_res) == "l"

        w_res = space.execute("return 'hello'[-6]")
        assert self.unwrap(space, w_res) is None

        w_res = space.execute("return 'hello'[-2..0]")
        assert self.unwrap(space, w_res) == ""

        w_res = space.execute("return 'hello'[5..5]")
        assert self.unwrap(space, w_res) == ""

        w_res = space.execute("return 'hello'[5..8]")
        assert self.unwrap(space, w_res) == ""

        w_res = space.execute("return 'hello'[-3..-2]")
        assert self.unwrap(space, w_res) == "ll"

        w_res = space.execute("return 'hello'[-2..-1]")
        assert self.unwrap(space, w_res) == "lo"

        w_res = space.execute("return 'hello'[4..2]")
        assert self.unwrap(space, w_res) == ""

        w_res = space.execute("return 'hello'[8..10]")
        assert self.unwrap(space, w_res) is None

        w_res = space.execute("return 'hello'[3..-2]")
        assert self.unwrap(space, w_res) == "l"

        w_res = space.execute("return 'hello'[-2..0]")
        assert self.unwrap(space, w_res) == ""

        w_res = space.execute("return 'hello'[-2...1]")
        assert self.unwrap(space, w_res) == ""

    def test_succ(self, space):
        w_res = space.execute("return 'a'.succ")
        assert self.unwrap(space, w_res) == "b"

    def test_object_id(self, space):
        w_res = space.execute("return 'asd'.object_id")
        assert self.unwrap(space, w_res) >= 0
