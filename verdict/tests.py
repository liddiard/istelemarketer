from django.test import TestCase
from verdict import scrapers


class EightHundredNotesTestCase(TestCase):

    def setUp(self):
        self.good_numbers = ['4802053588', '3102674357', '3108259898']
        self.bad_numbers = ['3179373100', '8662111876', '3309476028']

    def test_verdict(self):
        '''numbers are correctly identified as telemarketers or not'''
        for number in self.good_numbers:
            result = scrapers.eight_hundred_notes(number)
            print result
            self.assertEqual(result['verdict'], False)
        for number in self.bad_numbers:
            result = scrapers.eight_hundred_notes(number)
            print result
            self.assertEqual(result['verdict'], True)


class WhoCalledUsTestCase(TestCase):

    def setUp(self):
        self.good_numbers = ['4802053588', '3102674357', '3108259898']
        self.bad_numbers = ['2154293524', '213223126', '9540826973']

    def test_verdict(self):
        '''numbers are correctly identified as telemarketers or not'''
        for number in self.good_numbers:
            result = scrapers.who_called_us(number)
            print result
            self.assertEqual(result['verdict'], False)
        for number in self.bad_numbers:
            result = scrapers.who_called_us(number)
            print result
            self.assertEqual(result['verdict'], True)


class WhyCallMeTestCase(TestCase):

    def setUp(self):
        self.good_numbers = ['4802053588', '3102674357', '3108259898']
        self.bad_numbers = ['2392054843', '3176432452', '6181666752']

    def test_verdict(self):
        '''numbers are correctly identified as telemarketers or not'''
        for number in self.good_numbers:
            result = scrapers.why_call_me(number)
            print result
            self.assertEqual(result['verdict'], False)
        for number in self.bad_numbers:
            result = scrapers.why_call_me(number)
            print result
            self.assertEqual(result['verdict'], True)
