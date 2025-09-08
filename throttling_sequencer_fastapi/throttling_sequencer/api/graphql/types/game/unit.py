import strawberry


@strawberry.type
class CoordinateType:
    x: float
    y: float


@strawberry.type
class UnitType:
    coordinate: CoordinateType
    speed: float
    mass: float
    friction: float


@strawberry.input
class CoordinateInputType:
    x: float
    y: float


@strawberry.input
class UnitInputType:
    coordinate: CoordinateInputType
    speed: float
    mass: float
    friction: float
