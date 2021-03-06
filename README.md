[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/docs/faq/custom_repositories)
![GitHub Release](https://img.shields.io/github/release/anybody84/ha-nomics.svg?style=popout)
![GitHub Downloads](https://img.shields.io/github/downloads/anybody84/ha-nomics/total)

# Nomics Sensor

This is a custom Nomics integration which can be used in HomeAssistant.

## Example
![Example](https://github.com/anybody84/ha-nomics/blob/master/example.png)

## Getting Started
Before using the Nomics integration, sign up for a [free API key here](https://p.nomics.com/cryptocurrency-bitcoin-api).

## Installation using [HACS](https://hacs.xyz/)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/anybody84/ha-nomics`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface by going to **HACS** > **Integrations** > **Explore & Download Repositories and searching** for `Nomics`.


## Configuration

This can be done directly from the UI. Go to **Configuration** > **Integrations** > **Add Integration** and search for `Nomics`. 

You can also use the MyHomeAssistant link:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=nomics)


Please provide your `api_key` and other details in the configuration window as shown below:

![Config example](https://github.com/anybody84/ha-nomics/blob/master/config_example.png)

More details about the configuration options:

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
|`api_key`|`string`|`true`|-|Api key from the Nomics portal|
|`quote`|`list`|`true`|`BTC, ETH`|Comma-separated list of currency codes|
|`display_currency`|`string`|`false`|`USD`|The currency to use for diplaying exchange rates|
|`name`|`string`|`false`|`Nomics`|Integration name|
