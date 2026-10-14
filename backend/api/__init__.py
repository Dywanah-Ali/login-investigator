"""The HTTP API in front of the core. Routes validate input, call the core and shape the reply; they
hold no analysis. The core never imports this package. Contract: docs/api-contract.md.
"""
