# n8n-nodes-_kiwi-tcms_

This is an n8n community node. It lets you use _[Kiwi TCMS](https://kiwitcms.org/)_ in your n8n workflows.

Kiwi TCMS is an open source test case management system that helps teams manage test plans, test cases, and test runs, with full API access for automation and integration.

[n8n](https://n8n.io/) is a [fair-code licensed](https://docs.n8n.io/reference/license/) workflow automation platform.

[Installation](#installation)  
[Operations](#operations)  
[Credentials](#credentials)  <!-- delete if no auth needed -->  
[Compatibility](#compatibility)  
[Usage](#usage)  <!-- delete if not using this section -->  
[Resources](#resources)  
[Version history](#version-history)  <!-- delete if not using this section -->  

## 🛠 Installation

Follow the [official installation guide](https://docs.n8n.io/integrations/community-nodes/installation/) in the n8n documentation for community nodes.

Additionally, for this node to work properly:

### ✅ Requirements

* Python 3 must be installed and accessible via `python3`

* The `tcms-api` Python package must be installed:

  ```bash
  pip3 install tcms-api
  ```

* Ensure your n8n instance has access to this custom node by setting the environment variable:

  ```bash
  export N8N_CUSTOM_EXTENSIONS=/path/to/custom-nodes
  ```

  Or add it to your `.env`:

  ```
  N8N_CUSTOM_EXTENSIONS=/root/.n8n/custom-nodes
  ```

* Restart n8n after adding the custom node:

  ```bash
  pm2 restart n8n
  # or
  systemctl restart n8n
  ```


## 🧩 Operations

This node allows you to dynamically call any method from the [Kiwi TCMS XML-RPC API](https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html). Supported operations include:

* `TestCase.*` — create, update, filter test cases
* `TestPlan.*` — manage test plans and their relationships
* `TestRun.*` — manage and execute test runs
* `TestExecution.*` — track and annotate test executions
* `Product.*`, `Build.*`, `Component.*`, `Tag.*`, etc.

Simply choose an action from the dropdown and provide the corresponding parameters in JSON format.

---

## 🔐 Credentials

This node uses a custom credential type: **Kiwi TCMS API**

To set up credentials:

1. Go to **Credentials** in n8n.
2. Click **New**, then select **Kiwi TCMS API**.
3. Fill in:

   * **API URL** (e.g. `https://your-kiwi-tcms-instance/xml-rpc/`)
   * **Username**
   * **Password**

You must have a valid Kiwi TCMS user account. No OAuth or API token is required — just basic login credentials.

---

## 🧪 Compatibility

* ✅ Minimum n8n version: `1.80.0`
* ✅ Tested with:

  * n8n `1.90.2`
  * Python `3.11`
  * `tcms-api` Python package (latest)
* ⚠️ Known incompatibilities:

  * This node relies on having `python3` and `tcms-api` installed on the host machine
  * Not compatible with n8n cloud (due to Python execution)

---

## 🚀 Usage

1. Install Python 3 and the `tcms-api` library:

   ```bash
   pip3 install tcms-api
   ```

2. Make sure `tcms_script.py` is executable and accessible.

3. Set `N8N_CUSTOM_EXTENSIONS` to include the folder containing this node:

   ```
   export N8N_CUSTOM_EXTENSIONS=/root/.n8n/custom-nodes
   ```

4. Restart your n8n instance.

5. In a workflow, drag in the **Python TCMS** node, select an action (e.g. `TestCase.filter`), and enter JSON parameters:

   ```json
   {
     "pk": 123
   }
   ```

📚 If you're new to n8n, check out the [Try it out guide](https://docs.n8n.io/try-it-out/) to get started.


## Resources

* [n8n community nodes documentation](https://docs.n8n.io/integrations/community-nodes/)
* [Kiwi TCMS XML-RPC API](https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html)

## Version history
| Version | Description                                                                                                                                            | Compatibility                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| 1.0.0   | Initial release. Supports all major Kiwi TCMS XML-RPC methods dynamically.                                                                             | Requires `n8n >= 1.80.0`, Python 3.6+ |



