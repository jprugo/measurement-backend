from typing import List

import strawberry

from measurement.presentation.graphql.controller import CreateMutation, Queries
from measurement.presentation.graphql.schema import FilterInput, MeasurementType

#queries = Queries()  # Instancia de la clase Queries

#@strawberry.type
#class Mutation:
#    create_mutation = CreateMutation()
#    add_measurement: MeasurementType = strawberry.mutation(resolver=create_mutation.add_measurement)


#@strawberry.type(description="Measurements query", name="Measurement")
#class Query:
#    @strawberry.field(description="returns all the measurements from database and has the ability to filter through criteria")
#    def getAllMeasurements(self, where: FilterInput = None) -> List[MeasurementType]:
#        return queries.get_all_measurements(**vars(where))