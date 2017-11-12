from graphene.types import Scalar


class LocationScalar(Scalar):
    @staticmethod
    def serialize(location):
        return {'lat': location['lat'], 'lng': location['lng']}
