Custom Content Integration for Home Assistant
This custom integration for Home Assistant allows you to store large blocks of text with a title and automatically tracks the last update time. The content can then be displayed in markdown cards on your dashboards.

Features
Store large blocks of text/markdown content
Track when content was last updated
Set a title for your content
Update content via service calls
Easy integration with dashboard markdown cards
Installation
HACS Installation (Recommended)
Make sure HACS is installed in your Home Assistant instance.
Add this repository as a custom repository in HACS:
Go to HACS > Integrations
Click the three dots in the upper right corner
Select "Custom repositories"
Add the URL of this repository and select "Integration" as the category
Click "Install" on the Custom Content integration card
Restart Home Assistant
Manual Installation
Download the latest release from the repository
Create a custom_components/custom_markdown directory in your Home Assistant configuration folder
Extract the contents of the release into the custom_markdown directory
Restart Home Assistant
Configuration
Using the UI
Go to Configuration > Integrations
Click the "Add Integration" button
Search for "Custom Content"
Follow the setup wizard
Using YAML Configuration
Add the following to your configuration.yaml:

yaml
sensor:
  - platform: custom_markdown
    name: "My Content"  # Name of the sensor
    initial_title: "Welcome"  # Initial title for the content
    initial_content: |  # Initial content (can be blank)
      # Welcome to my dashboard
      This is some **markdown** content that can be quite large.
Usage
Updating Content via Service
You can update the content and title using the custom_markdown.update_content service:

yaml
service: custom_markdown.update_content
data:
  entity_id: sensor.my_content
  content: |
    # New Content
    This is the updated content with **markdown** formatting.
    
    ## It can have headers
    
    - And lists
    - Of items
  title: "New Title"  # Optional
Displaying Content in a Dashboard
Create a markdown card in your dashboard:

yaml
type: markdown
content: |
  # {{ states('sensor.my_content') }}
  Last updated: {{ state_attr('sensor.my_content', 'last_updated') }}
  
  {{ state_attr('sensor.my_content', 'content') }}
Or just display the content without the title:

yaml
type: markdown
content: "{{ state_attr('sensor.my_content', 'content') }}"
Example Automation
Here's an example automation to update content on a schedule:

yaml
automation:
  - alias: "Update Dashboard Content Daily"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      service: custom_markdown.update_content
      data:
        entity_id: sensor.my_content
        title: "Daily Update - {{ now().strftime('%Y-%m-%d') }}"
        content: |
          # Daily Dashboard Update
          
          Today is {{ now().strftime('%A, %B %d') }}
          
          ## Reminders:
          - Take out the trash
          - Water the plants
License
This project is licensed under the MIT License - see the LICENSE file for details.

