import math
import logging


class BaseNumber:
    @classmethod
    def from_string(cls, value: str) -> "BaseNumber":
        raise NotImplementedError()

    def to_string(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.to_string()


class BaseOperation:
    def apply(self, first: BaseNumber, second: BaseNumber) -> BaseNumber:
        raise NotImplementedError()


class BaseOperationFactory:
    def create_addition(self) -> BaseOperation:
        raise NotImplementedError()

    def create_subtraction(self) -> BaseOperation:
        raise NotImplementedError()

    def create_multiplication(self) -> BaseOperation:
        raise NotImplementedError()

    def create_division(self) -> BaseOperation:
        raise NotImplementedError()

    def create(self, operation: str) -> BaseOperation:
        if operation == "+":
            return self.create_addition()
        elif operation == "-":
            return self.create_subtraction()
        elif operation == "*":
            return self.create_multiplication()
        elif operation == "/":
            return self.create_division()
        else:
            raise ValueError(f"Invalid operation: {operation}")


# https://en.wikipedia.org/wiki/Complex_number
class ComplexNumber(BaseNumber):
    @classmethod
    def from_string(cls, value: str) -> "ComplexNumber":
        real, img = value.split(",")
        real = float(real.strip())
        img = float(img.strip())
        return ComplexNumber(real=real, img=img)

    def __init__(self, real: float, img: float):
        self._real = real
        self._img = img

    @property
    def real(self) -> float:
        return self._real

    @property
    def img(self) -> float:
        return self._img

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.real ** 2 + self.img ** 2)

    def to_string(self) -> str:
        real = self.real
        img_abs = abs(self._img)
        img_sign = "+" if self._img >= 0 else "-"

        return f"{real}{img_sign}{img_abs}i"


class BaseComplexOperation(BaseOperation):
    def apply(self, first: ComplexNumber, second: ComplexNumber) -> ComplexNumber:
        raise NotImplementedError()


# https://en.wikipedia.org/wiki/Complex_number#Addition_and_subtraction
class ComplexAddition(BaseComplexOperation):
    def apply(self, first: ComplexNumber, second: ComplexNumber) -> ComplexNumber:
        result_real = first.real + second.real
        result_img = first.img + second.img
        return ComplexNumber(real=result_real, img=result_img)


# https://en.wikipedia.org/wiki/Complex_number#Addition_and_subtraction
class ComplexSubtraction(BaseComplexOperation):
    def apply(self, first: ComplexNumber, second: ComplexNumber) -> ComplexNumber:
        result_real = first.real - second.real
        result_img = first.img - second.img
        return ComplexNumber(real=result_real, img=result_img)


# https://en.wikipedia.org/wiki/Complex_number#Multiplication
class ComplexMultiplication(BaseComplexOperation):
    def apply(self, first: ComplexNumber, second: ComplexNumber) -> ComplexNumber:
        result_real = first.real * second.real - first.img * second.img
        result_img = first.real * second.img + first.img * second.real
        return ComplexNumber(real=result_real, img=result_img)


# https://en.wikipedia.org/wiki/Complex_number#Complex_conjugate,_absolute_value_and_argument
class ComplexDivision(BaseComplexOperation):
    def apply(self, first: ComplexNumber, second: ComplexNumber) -> ComplexNumber:
        denominator = second.magnitude ** 2

        if denominator == 0:
            raise ZeroDivisionError("Division by zero is not allowed for complex numbers")

        result_real = (first.real * second.real + first.img * second.img) / denominator
        result_img = (first.img * second.real - first.real * second.img) / denominator
        return ComplexNumber(real=result_real, img=result_img)


class ComplexOperationFactory(BaseOperationFactory):
    def create_addition(self) -> ComplexAddition:
        return ComplexAddition()

    def create_subtraction(self) -> ComplexSubtraction:
        return ComplexSubtraction()

    def create_multiplication(self) -> ComplexMultiplication:
        return ComplexMultiplication()

    def create_division(self) -> ComplexDivision:
        return ComplexDivision()


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("calculator")

    logger.info(f"Калькулятор комплексных числел")
    operation_factory = ComplexOperationFactory()

    while True:
        try:
            logger.info(f"Введите операцию (+,-,*,/) или q для выхода:")
            operation = input()

            if operation == "q":
                logger.info("Выход")
                break

            operation = operation_factory.create(operation)

            logger.info(f"Введите первое комплексное число в формате a,b:")
            first = input()
            first = ComplexNumber.from_string(first)

            logger.info(f"Введите второе комплексное число в формате c,d:")
            second = input()
            second = ComplexNumber.from_string(second)

            result = operation.apply(first, second)
            logger.info(f"Результат: {result}")

        except Exception as exc:
            logger.error(f"Произошла ошибка: {exc}")


if __name__ == "__main__":
    main()
