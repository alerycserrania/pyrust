from unittest import TestCase

from src.pyrust_alerycserrania import Err, Nothing, Ok, Panic, Some, as_result


class TestResult(TestCase):
    def test_bool(self):
        self.assertTrue(Some(5))
        self.assertTrue(Some(True))
        self.assertFalse(Some(False))
        self.assertFalse(Some(0))
        self.assertFalse(Some(""))
        self.assertFalse(Nothing())

    def test_eq(self):
        self.assertTrue(Ok(4) == Ok(4))
        self.assertFalse(Ok(4) == Ok(5))
        self.assertFalse(Ok(4) == Ok("5"))
        self.assertTrue(Err("aie") == Err("aie"))
        self.assertFalse(Err("aid") == Err("aie"))
        self.assertFalse(Err("aie") == Ok(5))
        self.assertFalse(Ok(5) == Err("aie"))

    def test_neq(self):
        self.assertFalse(Ok(4) != Ok(4))
        self.assertTrue(Ok(4) != Ok(5))
        self.assertTrue(Ok(4) != Ok("5"))
        self.assertFalse(Err("aie") != Err("aie"))
        self.assertTrue(Err("aie") != Ok(5))
        self.assertTrue(Ok(5) != Err("aie"))

    def test_lt(self):
        self.assertTrue(Ok(4) < Ok(5))
        self.assertFalse(Ok(4) < Ok(4))
        self.assertFalse(Ok(5) < Ok(4))

        self.assertTrue(Ok(4) < Err("aie"))
        self.assertFalse(Err("aie") < Ok(4))
        self.assertTrue(Err("aie") < Err("aif"))
        self.assertFalse(Err("aie") < Err("aie"))
        self.assertFalse(Err("aie") < Err("aid"))

    def test_gt(self):
        self.assertFalse(Ok(4) > Ok(5))
        self.assertFalse(Ok(4) > Ok(4))
        self.assertTrue(Ok(5) > Ok(4))

        self.assertFalse(Ok(4) > Err("aie"))
        self.assertTrue(Err("aie") > Ok(4))
        self.assertFalse(Err("aie") > Err("aif"))
        self.assertFalse(Err("aie") > Err("aie"))
        self.assertTrue(Err("aie") > Err("aid"))

    def test_lte(self):
        self.assertTrue(Ok(4) <= Ok(5))
        self.assertTrue(Ok(4) <= Ok(4))
        self.assertFalse(Ok(5) <= Ok(4))

        self.assertTrue(Ok(4) <= Err("aie"))
        self.assertFalse(Err("aie") <= Ok(4))
        self.assertTrue(Err("aie") <= Err("aif"))
        self.assertTrue(Err("aie") <= Err("aie"))
        self.assertFalse(Err("aie") <= Err("aid"))

    def test_gte(self):
        self.assertFalse(Ok(4) >= Ok(5))
        self.assertTrue(Ok(4) >= Ok(4))
        self.assertTrue(Ok(5) >= Ok(4))

        self.assertFalse(Ok(4) >= Err("aie"))
        self.assertTrue(Err("aie") >= Ok(4))
        self.assertFalse(Err("aie") >= Err("aif"))
        self.assertTrue(Err("aie") >= Err("aie"))
        self.assertTrue(Err("aie") >= Err("aid"))

        self.assertRaises(TypeError, lambda: Ok(4) > Ok("a"))
        self.assertRaises(TypeError, lambda: Ok(6) >= 5)

    def test_is_ok(self):
        self.assertTrue(Ok(5).is_ok())
        self.assertFalse(Err("oh no!").is_ok())

    def test_is_ok_and(self):
        self.assertTrue(Ok(5).is_ok_and(lambda x: x > 1))
        self.assertFalse(Ok(-3).is_ok_and(lambda x: x > 1))
        self.assertFalse(Err("oh no!").is_ok_and(lambda x: x > 1))

    def test_is_err(self):
        self.assertFalse(Ok(5).is_err())
        self.assertTrue(Err("oh no!").is_err())

    def test_is_err_and(self):
        self.assertFalse(Ok(5).is_err_and(lambda x: len(x) == 6))
        self.assertFalse(Err("oh...").is_err_and(lambda x: len(x) == 6))
        self.assertTrue(Err("oh no!").is_err_and(lambda x: len(x) == 6))

    def test_ok(self):
        self.assertEqual(Ok(2).ok(), Some(2))
        self.assertEqual(Err("oh no!").ok(), Nothing())

    def test_err(self):
        self.assertEqual(Ok(2).err(), Nothing())
        self.assertEqual(Err("oh no!").err(), Some("oh no!"))

    def test_map(self):
        self.assertEqual(Ok(2).map(lambda x: x * 2), Ok(4))
        self.assertEqual(Err("oh no!").map(lambda x: x * 2), Err("oh no!"))

    def test_map_or(self):
        self.assertEqual(Ok(2).map_or("yes", lambda x: x * 2), 4)
        self.assertEqual(Err("oh no!").map_or("ah", lambda x: x * 2), "ah")

    def test_map_or_else(self):
        k = 10
        self.assertEqual(Ok(2).map_or_else(lambda: k, lambda x: x * 2), 4)
        self.assertEqual(Err("oh no!").map_or_else(lambda: k, lambda x: x * 2), 10)

    def test_map_err(self):
        self.assertEqual(Ok(2).map_err(lambda x: len(x)), Ok(2))
        self.assertEqual(Err("oh no!").map_err(lambda x: len(x)), Err(6))

    def test_inspect(self):
        self.assertEqual(Ok(4).inspect(lambda v: self.assertEqual(v, 4)), Ok(4))
        self.assertEqual(
            Err("oh no!").inspect(
                lambda _: self.fail("Nothing should not be inspected")
            ),
            Err("oh no!"),
        )

    def test_inspect_err(self):
        self.assertEqual(
            Ok(4).inspect_err(lambda _: self.fail("Nothing should not be inspected")),
            Ok(4),
        )
        self.assertEqual(
            Err("oh no!").inspect(lambda v: self.assertEqual(v, "oh no!")),
            Err("oh no!"),
        )

    def test_expect(self):
        self.assertEqual(Ok("value").expect("expected value"), "value")
        with self.assertRaises(Panic, msg="expected value"):
            Err(5).expect("expected value")

    def test_unwrap(self):
        self.assertEqual(Ok("value").unwrap(), "value")
        self.assertRaises(Panic, Err(5).unwrap)

    def test_expect_err(self):
        self.assertEqual(Err("value").expect_err("expected error"), "value")
        with self.assertRaises(Panic, msg="expected error"):
            Ok(5).expect_err("expected error")

    def test_unwrap_err(self):
        self.assertEqual(Err("value").unwrap_err(), "value")
        self.assertRaises(Panic, Ok(5).unwrap_err)

    def test_as_result(self):
        @as_result
        def my_func(x: int):
            if x > 0:
                return x * 2
            else:
                raise Exception("X must be ")

        self.assertEqual(my_func(5), Ok(10))
        self.assertEqual(str(my_func(-1).unwrap_err()), "X must be ")

    def test_as_result_bases(self):
        @as_result((TypeError,))
        def my_func(x: int):
            if x > 0:
                return x * 2
            elif x > -5:
                raise TypeError("x must be greater than 0")
            else:
                raise Exception("oh no.")

        self.assertEqual(my_func(5), Ok(10))
        self.assertEqual(str(my_func(-1).unwrap_err()), "x must be greater than 0")
        self.assertRaises(Exception, my_func, -6)
