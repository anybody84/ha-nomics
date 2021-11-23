[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/docs/faq/custom_repositories)
![GitHub All Releases](https://img.shields.io/github/downloads/anybody84/ha-nomics/total)

# Nomics Sensor

This is a custom Nomics integration which can be used in HomeAssistant.

## Example
![example](https://github.com/anybody84/ha-nomics/blob/master/example.png)

## Getting Started
Before using the Nomics integration, sign up for a [free API key here](https://p.nomics.com/cryptocurrency-bitcoin-api).

## Installation

### Using [HACS](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):
* URL: `https://github.com/anybody84/ha-nomics`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

### Manual

To install this integration manually you have to download [*nomics.zip*](https://github.com/anybody84/ha-nomics/releases/latest/download/nomics.zip) extract its contents to `config/custom_components/nomics` directory. Navigate to the `config` directory and run the following commands:
```bash
mkdir custom_components
cd custom_components
wget https://github.com/anybody84/ha-nomics/releases/latest/download/nomics.zip
unzip nomics.zip
rm nomics.zip
```

## Configuration

| Key | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
|`api_key`|`string`|`true`|-|Api key from the Nomics portal|
|`quote`|`list`|`true`|-|List of currency codes|
|`display_currency`|`string`|`false`|`USD`|The currency to use for diplaying exchange rates|

### Example configuration

```yaml
sensor:
  - platform: nomics
    api_key: "this-is-your-api-key"
    quote:
      - ETH
      - BTC
    display_currency: PLN
```
