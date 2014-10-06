#!/usr/bin/env python
#
# Copyright 2013 Ravi Rajamani.

import sys

from splunklib.modularinput import *

class CeilometerIntegrationScript(Script):


SCHEME = """<scheme>
    <title>Ceilometer Telemetry</title>
    <description>Get data from Ceilometer.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>

    <endpoint>
        <args>
            <arg name="msg">
                <title>Message from a publishing sample</title>
                <description> This is typically the meter message from counter that pertains to a sample from pipeline
                </description>
            </arg>

            <arg name="secret">
                <title>Metering Secret</title>
                <description>This is the publisher secret </description>
                <validation>
validate(match('ssn', '^\s{15}$'), "Secret is not in valid format")
</validation>
            </arg>

            <arg name="host">
                <title>IPv4 address of host</title>
                <description>This is the host that receives the Ceilometer data</description>
                <validation>
validate(match(host, '(?<ip>[[(?:2(?:5[0-5]|[0-4][0-9])|[0-1][0-9][0-9]|[0-9][0-9]?)]](?:\.[[ (?:2(?:5[0-5]|[0-4][0-9])|[0-1][0-9][0-9]|[0-9][0-9]?)]]){3}), "host is not in valid format")
</validation>
            </arg>

            <arg name="port">
                <title>UDP port</title>
                <description>This is the port on which the host is listening</description>
                <validation>is_avail_udp_port(port) </validation>
            </arg>

        </args>
    </endpoint>
</scheme>
"""


    def do_scheme():
         print SCHEME

    def get_scheme(self):
        scheme = Scheme("Ceilometer Telemetry")

        scheme.description = "Streams events from Ceilometer."
        scheme.use_external_validation = True
        scheme.use_single_instance = True
        scheme.validation = ""

        ceilometer_argument = Argument("data_from_ceilometer")
        ceilometer_argument.data_type = Argument.data_type_string
        ceilometer_argument.description = "Telemetry data from Ceilometer to be produced by this input."
        ceilometer_argument.required_on_create = True

        return scheme

    def validate_input(self, validation_definition):
        data = str(validation_definition.parameters["data_from_ceilometer"])

        if not data:
            raise ValueError("Ceilometer data could not be read.")

    def stream_events(self, inputs, ew):
        """This function handles all the action: splunk calls this modular input
        without arguments, streams XML describing the inputs to stdin, and waits
        :param inputs: an InputDefinition object
        :param ew: an EventWriter object
        """
        for input_name, input_item in inputs.inputs.iteritems():

            # Create an Event object, and set its data fields
            event = Event()
            event.stanza = input_name
            event.data = "number=\"%s\"" % str(input_item["data_from_ceilometer"])

            # Tell the EventWriter to write this event
            ew.write_event(event)

    if __name__ == "__main__":
	if len(sys.argv) > 1:
            if sys.argv[1] == "--scheme":
               do_scheme()
        sys.exit(CeilometerIntegrationScript().run(sys.argv))
