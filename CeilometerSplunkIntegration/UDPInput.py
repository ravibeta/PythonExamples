#!/usr/bin/env python
#
# Copyright 2013 Ravi Rajamani.

import sys

from splunklib.modularinput import *

class CeilometerIntegrationScript(Script):
    def get_scheme(self):
        scheme = Scheme("Ceilometer Telemetry")

        scheme.description = "Streams events from Ceilometer."
        scheme.use_external_validation = True
        scheme.use_single_instance = True
        scheme.validation = ""

        return scheme

    def validate_input(self, validation_definition):
        minimum = float(validation_definition.parameters["min"])
        maximum = float(validation_definition.parameters["max"])

        if minimum >= maximum:
            raise ValueError("min must be less than max; found min=%f, max=%f" % minimum, maximum)

    def stream_events(self, inputs, ew):
        """This function handles all the action: splunk calls this modular input
        without arguments, streams XML describing the inputs to stdin, and waits
        :param inputs: an InputDefinition object
        :param ew: an EventWriter object
        """
        # Go through each input for this modular input
        for input_name, input_item in inputs.inputs.iteritems():
            # Get the values, cast them as floats
            minimum = float(input_item["min"])
            maximum = float(input_item["max"])

            # Create an Event object, and set its data fields
            event = Event()
            event.stanza = input_name
            event.data = "number=\"%s\"" % str(random.uniform(minimum, maximum))

            # Tell the EventWriter to write this event
            ew.write_event(event)

if __name__ == "__main__":
    sys.exit(CeilometerIntegrationScript().run(sys.argv))
