from unittest import TestCase

from src.pyrust_alerycserrania import Err, Nothing, Ok, Panic, Result, Some, as_option


class TestOption(TestCase):
    def test_bool(self):
        self.assertTrue(Some(5))
        self.assertTrue(Some(True))
        self.assertFalse(Some(False))
        self.assertFalse(Some(0))
        self.assertFalse(Some(""))
        self.assertFalse(Nothing())

    def test_eq(self):
        self.assertTrue(Some(4) == Some(4))
        self.assertFalse(Some(4) == Some(5))
        self.assertFalse(Some(4) == Some("5"))
        self.assertTrue(Nothing() == Nothing())
        self.assertFalse(Nothing() == Some(5))
        self.assertFalse(Some(5) == Nothing())

    def test_neq(self):
        self.assertFalse(Some(4) != Some(4))
        self.assertTrue(Some(4) != Some(5))
        self.assertTrue(Some(4) != Some("5"))
        self.assertFalse(Nothing() != Nothing())
        self.assertTrue(Nothing() != Some(5))
        self.assertTrue(Some(5) != Nothing())

    def test_lt(self):
        self.assertTrue(Some(4) < Some(5))
        self.assertFalse(Some(4) < Some(4))
        self.assertFalse(Some(5) < Some(4))

        self.assertFalse(Some(4) < Nothing())
        self.assertTrue(Nothing() < Some(4))
        self.assertFalse(Nothing() < Nothing())

    def test_gt(self):
        self.assertFalse(Some(4) > Some(5))
        self.assertFalse(Some(4) > Some(4))
        self.assertTrue(Some(5) > Some(4))

        self.assertTrue(Some(4) > Nothing())
        self.assertFalse(Nothing() > Some(4))
        self.assertFalse(Nothing() > Nothing())

    def test_lte(self):
        self.assertTrue(Some(4) <= Some(5))
        self.assertTrue(Some(4) <= Some(4))
        self.assertFalse(Some(5) <= Some(4))

        self.assertFalse(Some(4) <= Nothing())
        self.assertTrue(Nothing() <= Some(4))
        self.assertTrue(Nothing() <= Nothing())

    def test_gte(self):
        self.assertFalse(Some(4) >= Some(5))
        self.assertTrue(Some(4) >= Some(4))
        self.assertTrue(Some(5) >= Some(4))

        self.assertTrue(Some(4) >= Nothing())
        self.assertFalse(Nothing() >= Some(4))
        self.assertTrue(Nothing() >= Nothing())

    def test_is_some(self):
        self.assertTrue(Some(2).is_some())
        self.assertFalse(Nothing().is_some())

    def test_is_some_and(self):
        self.assertTrue(Some(2).is_some_and(lambda x: x > 1))
        self.assertFalse(Some(0).is_some_and(lambda x: x > 1))
        self.assertFalse(Nothing().is_some_and(lambda x: x > 1))

    def test_is_nothing(self):
        self.assertFalse(Some(2).is_nothing())
        self.assertTrue(Nothing().is_nothing())

    def test_expect(self):
        self.assertEqual(Some("value").expect("expected value"), "value")
        with self.assertRaises(Panic, msg="expected value"):
            Nothing().expect("expected value")

    def test_unwrap(self):
        self.assertEqual(Some("value").unwrap(), "value")
        self.assertRaises(Panic, Nothing().unwrap)

    def test_unwrap_or(self):
        self.assertEqual(Some("value").unwrap_or("default"), "value")
        self.assertEqual(Nothing().unwrap_or("default"), "default")

    def test_unwrap_or_else(self):
        k = 5
        self.assertEqual(Some(5).unwrap_or_else(lambda: 2 * k), 5)
        self.assertEqual(Nothing().unwrap_or_else(lambda: 2 * k), 10)

    def test_map(self):
        self.assertEqual(
            Some("hello world").map(lambda x: x.split()), Some(["hello", "world"])
        )
        self.assertEqual(Nothing().map(lambda x: x.split()), Nothing())

    def test_inspect(self):
        self.assertEqual(
            Some(4).inspect(lambda v: self.assertEqual(v, 4)), Some(4)
        )
        self.assertEqual(
            Nothing().inspect(lambda _: self.fail("Nothing should not be inspected")), Nothing()
        )

    def test_map_or(self):
        self.assertEqual(Some(5).map_or("no", lambda x: str(x)), "5")
        self.assertEqual(Nothing().map_or("no", lambda x: x * 3), "no")

    def test_map_or_else(self):
        k = "no"
        self.assertEqual(Some(5).map_or_else(lambda: k, lambda x: str(x)), "5")
        self.assertEqual(Nothing().map_or_else(lambda: k, lambda x: x * 3), "no")

    def test_and_(self):
        self.assertEqual(Some(2).and_(Nothing()), Nothing())
        self.assertEqual(Nothing().and_(Some(2)), Nothing())
        self.assertEqual(Some(2).and_(Some("5")), Some("5"))
        self.assertEqual(Nothing().and_(Nothing()), Nothing())

    def test_and_then(self):
        self.assertEqual(Some(2).and_then(lambda x: Some(str(x * 2))), Some("4"))
        self.assertEqual(Nothing().and_then(lambda x: Some(str(x * 2))), Nothing())

    def test_filter(self):
        self.assertEqual(Nothing().filter(lambda x: x % 2 == 0), Nothing())
        self.assertEqual(Some(6).filter(lambda x: x % 2 == 0), Some(6))
        self.assertEqual(Some(5).filter(lambda x: x % 2 == 0), Nothing())

    def test_or_(self):
        self.assertEqual(Some(2).or_(Nothing()), Some(2))
        self.assertEqual(Nothing().or_(Some(2)), Some(2))
        self.assertEqual(Some(2).or_(Some("5")), Some(2))
        self.assertEqual(Nothing().or_(Nothing()), Nothing())

    def test_or_else(self):
        self.assertEqual(Some(2).or_else(lambda: Some("5")), Some(2))
        self.assertEqual(Nothing().or_else(lambda: Some("5")), Some("5"))
        self.assertEqual(Nothing().or_else(lambda: Nothing()), Nothing())

    def test_xor(self):
        self.assertEqual(Some(2).xor(Some(3)), Nothing())
        self.assertEqual(Nothing().xor(Some(3)), Some(3))
        self.assertEqual(Some(2).xor(Nothing()), Some(2))
        self.assertEqual(Nothing().xor(Nothing()), Nothing())

    def test_ok_or(self):
        self.assertEqual(Some(2).ok_or("error"), Ok(2))
        self.assertEqual(Nothing().ok_or("error"), Err("error"))

    def test_ok_or_else(self):
        self.assertEqual(Some(2).ok_or_else(lambda: "error"), Ok(2))
        self.assertEqual(Nothing().ok_or_else(lambda: "error"), Err("error"))

    def test_as_option(self):
        @as_option
        def my_func(x: int):
            return x if x > 0 else None

        self.assertEqual(my_func(5), Some(5))
        self.assertEqual(my_func(-1), Nothing())

        self.assertEqual(as_option(5), Some(5))
        self.assertEqual(as_option(None), Nothing())
