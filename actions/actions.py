# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
# from lxml import etree, html
from io import StringIO
# import asyncio
from rasa_sdk.types import DomainDict
import requests
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

# class invform(FormAction):
#     def name(self):
#         """Unique identifier of the form"""
#         return "inv_form"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["invoice_nbr"]

#     # def slot_mappings(self) -> Dict[Text: Union[Dict, List[Dict]]]:
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""

#         return {
#             "invoice_nbr": [self.from_entity(entity="invoice_nbr"), self.from_text()]
#             # "x12data": [self.from_text()]
#         }

#     def submit(self,
#                dispatcher: CollectingDispatcher,
#                tracker: Tracker,
#                domain: Dict[Text, Any]) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         # utter submit template
#         dispatcher.utter_template('utter_processing', tracker)
#         return []

class ValidateInvForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_inv_form"
        
    def validate_invoice_nbr(self, 
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> Dict[Text, Any]:

        # print ("Getting invoice details", tracker.get_slot('invoice_nbr'), "|", tracker.get_latest_entity_values("invoice_nbr"))
        # invoice_nbr = tracker.get_slot('invoice_nbr')
        # if str(slot_value.upper()).__len__().__ne__(9):
        #     dispatcher.utter_message(text=f"Invoice number should consist of 9 chars only")
        #     return {"invoice_nbr":None}
        return {"invoice_nbr":slot_value}

class ActionGetInvDetails(Action):
    def name(self) -> Text:
        return "action_get_inv_details"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print ("===== >>>> Getting invoice details", tracker.get_slot('invoice_nbr'), "|", next(tracker.get_latest_entity_values("invoice_nbr")))
        # invoice_nbr = tracker.get_slot('invoice_nbr')
        invoice_nbr = next(tracker.get_latest_entity_values("invoice_nbr"), None)
        print (f"Query params are: key-{invoice_nbr}")

        url = f"http://localhost:7002/get-invoice-details/"
        resp = requests.post(url, json={'invoice_nbr':invoice_nbr})
        print (resp.json())

        print ("Api response:", resp.status_code)
        if resp.ok:
            resp_data = resp.json()
            final_resp = "\n \t - Payment status: {} \n \t - Payment Date: {} \n \t - PO_NBR: {}".format(
                resp_data['resp_payload']['payment_sts'],
                str(resp_data['resp_payload']['payment_dt']),
                resp_data['resp_payload']['po'])
            print (f"Invoice fetch is successful-------{resp} | {resp_data['resp_payload']['payment_sts']} ")
        else:
            print ("Error occurred | During invoice data fetch : %s", resp.status)
            final_resp = "\n Error while fetching from the DB".format(invoice_nbr)

        print ("DB call done...")
        # dispatcher.utter_message(template='utter_clm_details', tracker=Tracker, icndata=str(u2_data[0]))  # Not working
        dispatcher.utter_template('utter_inv_details',tracker=Tracker, invoice_nbr=invoice_nbr, invdata=str(final_resp))
        
        # return {"invoice_nbr":None}
        return []


class ActionResetAllButFewSlots(Action):
    
    def name(self) -> Text:
        return "action_reset_all_slots"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print ("resetting..")
        return [AllSlotsReset()]