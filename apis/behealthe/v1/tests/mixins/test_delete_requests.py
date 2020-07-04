from apis.betterself.v1.tests.test_base import GenericRESTMethodMixin


class DeleteRequestsTestsMixinV2(GenericRESTMethodMixin):
    """
    Because you're kind of weird/lazy, the way you handle deletes are passing a delete to the endpoint
    querying the object and then deleting it
    """

    def test_delete_object(self):
        response = self.client_1.get(self.url)
        results = self._get_results_from_response(response)
        self.assertTrue(len(results) > 0)

        uuids = {item['uuid'] for item in results}

        for uuid in uuids:
            data = {'uuid': uuid}
            response = self.client_1.delete(self.url, data=data)
            self.assertEqual(response.status_code, 204, response)

        # now after we've deleted everything, when we try to get a get, we should get nothing
        response = self.client_1.get(self.url)
        results = self._get_results_from_response(response)

        self.assertEqual(len(results), 0)

    def test_deleting_object_that_doesnt_belong_to_you(self):
        response = self.client_1.get(self.url)
        results = self._get_results_from_response(response)
        original_count = len(results)

        uuids = {item['uuid'] for item in results}

        for uuid in uuids:
            data = {'uuid': uuid}
            response = self.client_2.delete(self.url, data=data)
            self.assertEqual(response.status_code, 404, response)

        response = self.client_1.get(self.url)
        results = self._get_results_from_response(response)
        after_delete_count = len(results)

        self.assertEqual(original_count, after_delete_count)
