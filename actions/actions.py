# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
# from lxml import etree, html
from io import StringIO
# import asyncio
# import aiohttp
# import requests
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class invform(FormAction):
    def name(self):
        """Unique identifier of the form"""
        return "inv_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["invoice_nbr"]

    # def slot_mappings(self) -> Dict[Text: Union[Dict, List[Dict]]]:
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "invoice_nbr": [self.from_text()]
            # "x12data": [self.from_text()]
        }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        dispatcher.utter_template('utter_processing', tracker)
        return []


class ActionGetClmDetails(Action):
    def name(self) -> Text:
        return "action_get_inv_details"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print ("Getting invoice details")
        # icn_metadata = next(tracker.get_latest_entity_values("clm_metadata"),None)
        # icn_metadata = tracker.latest_message.get('text')
        invoice_nbr = tracker.get_slot('invoice_nbr')
        # icn = str(icn_metadata)[0:10]
        # x12data = tracker.get_slot("x12data")
        # SlotSet('clm_nbr', icn)
        # tracker.get_slot('clm_nbr')
        print (f"Query params are: key-{invoice_nbr}")

        # url = f"http://opi-ude-claims-restapp-dev.optum.com/generate-u2/"
        # resp = requests.post(url, params={'key':icn,'metadata':icn_metadata,'value':x12data})
        resp = "{} payment status is PAID".format(invoice_nbr)

        # print ("Api response:", resp.status_code)
        # if resp.ok:
        #     tree = html.fromstring(resp.content)
        #     u2_data = tree.xpath('//textarea[@id="subject"]/text()')
        #     print (f"x12 conversion is successful------- {u2_data[0]}")
        # else:
        #     u2_data = resp.status_code
        #     print ("Response during x12 conversion is : %s", resp.status)

        print ("DB call done...")
        # dispatcher.utter_message(template='utter_clm_details', tracker=Tracker, icndata=str(u2_data[0]))  # Not working
        dispatcher.utter_template('utter_inv_details',tracker=Tracker, invoice_nbr=invoice_nbr, invdata=str(resp))
        
        return[]



class ActionResetAllButFewSlots(Action):
    
    def name(self) -> Text:
        return "action_reset_all_slots"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print ("resetting..")
        return [AllSlotsReset()]