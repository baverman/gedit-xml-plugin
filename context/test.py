# -*- coding: utf-8 -*-

import unittest

from context import get_position, guess_context, TagOpenContext, TagCloseContext

test_xml = u'''<?xml version="1.0"?>

<beans xmlns="http://farpost.com/slr/injector/schema"
	xmlns:async="http://farpost.com/slr/async/schema"
	xmlns:toolkit="http://farpost.com/slr/toolkit/injector-schema"
	xmlns:db="http://farpost.com/slr/db/injector-schema">
	
	<!-- <bean id="aaa" class="sss">
	</bean> -->
	
	<bean id="aaa" class="sss">
	    <aaa>
	    </aaa>
	</bean>
	
	<bean id="aaa" />
</beans>'''


class TestPositionGetter(unittest.TestCase):
    
    def testGetZeroPosition(self):
        self.assertEquals(0, get_position(0, 0, test_xml))
        self.assertEquals(0, get_position(1, 0, test_xml))    

    def testGetSomePosition(self):
       pos = get_position(3, 0, test_xml)
       self.assertEquals('<beans', test_xml[pos:pos+6]) 
       
       pos = get_position(3, 7, test_xml)
       self.assertEquals('xmlns', test_xml[pos:pos+5])
       
       pos = get_position(12, 5, test_xml)
       self.assertEquals('<aaa', test_xml[pos:pos+4])
       
       pos = get_position(12, 8, test_xml)
       self.assertEquals('a>', test_xml[pos:pos+2])


class TestContextGuesser(unittest.TestCase):
    def assertObjEquals(self, first, second):
        self.assertEquals(first.__class__, second.__class__)
        self.assertEquals(vars(first), vars(second))

    def testGuessContext(self):
        self.assertObjEquals(TagOpenContext('be', []), guess_context(3, 3, test_xml))
        self.assertObjEquals(TagOpenContext('beans', []), guess_context(3, 6, test_xml))
        self.assertObjEquals(TagOpenContext('beans', []), guess_context(3, 9, test_xml))
        
        self.assertObjEquals(TagOpenContext(None, ['beans']), guess_context(9, 5, test_xml))

if __name__ == '__main__':
    unittest.main()
