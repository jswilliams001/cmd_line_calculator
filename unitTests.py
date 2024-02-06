import unittest
from calc_simple import shunting_yard, calculate


class TestShuntingYard(unittest.TestCase):

    def test_valid_expression(self):
        infix_expression = "3 + 2 * 2"
        expected = (['3', '2', '2', '*', '+'], '3 + 2 * 2')
        actual = shunting_yard(infix_expression)
        self.assertEqual(actual, expected)

    def test_invalid_expression_chars(self):
        infix_expression = "3 + 2k * 2"
        expected = ([], '')
        actual = shunting_yard(infix_expression)
        self.assertEqual(actual, expected)

    def test_invalid_expression_dot(self):
        infix_expression = "3.1.1 + 2 * 2"
        expected = ([], '')
        actual = shunting_yard(infix_expression)
        self.assertEqual(actual, expected)

    def test_expression_with_parentheses(self):
        infix_expression = "(3 + 2) * 2"
        expected = (['3', '2', '+', '2', '*'], '( 3 + 2 ) * 2')
        actual = shunting_yard(infix_expression)
        self.assertEqual(actual, expected)

    def test_expression_with_unbalanced_parentheses(self):
        infix_expression = "(3 + 2 * 2"
        expected = ([], '')
        actual = shunting_yard(infix_expression)
        self.assertEqual(actual, expected)

    def test_expression_with_negative_values(self):
        infix_expression = "3 + -2 * 2"
        expected = (['3', '-2', '2', '*', '+'], '3 + -2 * 2')
        actual = shunting_yard(infix_expression)
        self.assertEqual(actual, expected)


class TestCalcSimple(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(calculate(["2", "3", "+"]), 5.0)

    def test_subtraction(self):
        self.assertEqual(calculate(["5", "3", "-"]), 2.0)

    def test_multiplication(self):
        self.assertEqual(calculate(["3", "4", "*"]), 12.0)

    def test_division(self):
        self.assertEqual(calculate(["12", "4", "/"]), 3.0)

    def test_multiple_operations(self):
        self.assertEqual(calculate(["3", "5", "+", "6", "*"]), 48.0)

    def test_invalid_input(self):
        self.assertEqual(calculate(["a", "+", "b"]), '')

    def test_not_enough_operators(self):
        self.assertEqual(calculate(["2", "2", "2", "+"]), '')

    def test_floating_point_numbers(self):
        self.assertEqual(calculate(["2.5", "2.5", "+"]), 5.0)

    def test_exp_modulo(self):
        self.assertEqual(calculate(['5', '2', '%', '43', '+', '-12', '-', '5', '3', '^', '+']), 181.0)

    def test_pi_approx(self):
        self.assertEqual(calculate(['335000022', '106633819', '/']), 3.1415926498890565)


if __name__ == "__main__":
    unittest.main()

