#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2021 Mattias Schlenker <ms@mattiasschlenker.de> for tribe29 GmbH
# License: GNU General Public License v2
#
# Reference for details:
# https://docs.checkmk.com/latest/en/devel_check_plugins.html
#
# This is the main CMK/server side script for a "Hello World!" Plugin

from .agent_based_api.v1 import *

# Most simple discovery function, basically just checks for the agents
# output containing a section named exactly as the service:

def discover_hello_bakery(section):
    yield Service()

# Thresholds are taken from the default parameters defined in
# ~/local/share/check_mk/web/plugins/wato/helloworld_parameters.py
# respectively overwritten by setup GUI settings.

def check_hello_bakery(params, section):
    for line in section:
        # Proving a Metric is the first step to get nice graphs, adding this line 
        # already allows you to create custom graphs using "hellolevel"
        #
        # If you want to define a default graph, look here:
        # ~/local/share/check_mk/web/plugins/metrics/hellobakery_metric.py
        # 
        # Everyone loves perf-o-meters, so take the next step and build one!
        #
        # ~/local/share/check_mk/web/plugins/perfometer/hellobakery_perfometer.py
        if line[0] == "hello_bakery":
            yield Metric(name="hellobakerylevel", value=float(line[1]), boundaries=(0.0, 100.0))
            
            # Two very simple transitions, both are not hardcoded.
            # Here we have to cast the string received to float. To cast, use a function
            # that fails early. CheckMK catches exceptions and changes state to UNKNOWN.
            # This is much better than casting the level of your bathtub to 0% allowing
            # more water to be poured in and not recognizing there might be a problem
            # that has to be investigated.
            if float(line[1]) > params["levels"][1]:
                yield Result(state=State.CRIT, summary="Hello, leave me alone!") 
                return
            elif float(line[1]) > params["levels"][0]:
                yield Result(state=State.WARN, summary="Hello, I need some coffee!")
                return
            yield Result(state=State.OK, summary="Hello bakery! What a lovely day.")

# Register the plugin with a unique name and define at least three functions!
# Default parameters can be left empty since defined elsewhere.

register.check_plugin(
    # This is some unique identifier! Do not use dumb terms like "hello_world" or
    # "updates_pending" since someone else might have had your idea and your and his 
    # or hers output is not parseable by your discovery/check function and vice versa! 
    name = "hello_bakery",
    # Nice human readable name. Be descriptive!
    service_name = "Hello bakery!",
    # Refer to the discovery function above.
    discovery_function = discover_hello_bakery,
    # Refer to the check function above.
    check_function = check_hello_bakery,
    # Refer to the ruleset defined in:
    # ~/local/share/check_mk/web/plugins/wato/hellobakery_parameters.py
    check_ruleset_name = "hello_bakery",
    # check_default_parameters = {}
    # if defaults have to be defined here, use:
    check_default_parameters = { "levels" : (80.0, 90.0) }
)

