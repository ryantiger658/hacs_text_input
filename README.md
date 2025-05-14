# Custom Markdown for Home Assistant

## Why I Built This

Ever tried to store a large block of text in Home Assistant for your dashboard? Frustrating, right?

I wanted to display blocks of LLM Markdown output on my Home Assistant dashboard. The problem was that Home Assistant's built-in text helpers have a 255-character limit. Way too small populating a markdown card. 

After trying various workarounds (template sensors, file reading, etc.), I decided to build a proper solution. This custom integration lets you store large markdown content that you can update through service calls and display beautifully on your dashboard.

No more character limits. No more complicated workarounds. Just simple markdown storage that works.

## What It Does

Custom Markdown gives you a sensor that:

1. Stores large blocks of markdown text (no character limit!)
2. Tracks when the content was last updated
3. Displays nicely on dashboards
4. Can be updated through simple service calls
5. Supports targeting for easy automation

It's perfect for:

- Workout routines
- Shopping lists
- Home instructions
- Project documentation
- Meeting notes
- Daily journal entries
- Anything text-based!
- LLM output

## Installation

### HACS Installation (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is already installed
2. Add this repository as a custom repository in HACS:
   - Go to HACS → Integrations
   - Click the three dots in the top-right corner
   - Select "Custom repositories"
   - Add the URL of this repository
   - Category: Integration
3. Click "Install" on the "Custom Markdown" card
4. Restart Home Assistant

### Manual Installation

1. Download this repository
2. Copy the `custom_components/custom_markdown` folder to your Home Assistant `config/custom_components` directory
3. Restart Home Assistant

## Setup

### Through the UI

1. Go to Settings → Devices & Services
2. Click "Add Integration" at the bottom-right
3. Search for "Custom Markdown"
4. Follow the setup prompts:
   - Name: What you want to call this content (e.g., "Workout Routine")
   - Initial Title: The title of the content
   - Initial Content: Optional starting content

### Through YAML Configuration

```yaml
# configuration.yaml
sensor:
  - platform: custom_markdown
    name: "Workout Routine"
    initial_title: "Monday Workout"
    initial_content: |
      # Monday Workout
      
      ## Warm-up
      - 5 minutes light cardio
      - Dynamic stretching
      
      ## Main Workout
      - Squats: 3 sets of 12
      - Push-ups: 3 sets of 15
      - Lunges: 3 sets of 10 each leg
```

## Using It

### Displaying the Content

Add a markdown card to your dashboard:

```yaml
type: markdown
content: "{{ state_attr('sensor.workout_routine', 'content') }}"
```

For more formatting, you can include the title and last updated time:

```yaml
type: markdown
content: |
  # {{ states('sensor.workout_routine') }}
  _Last updated: {{ state_attr('sensor.workout_routine', 'last_updated') }}_
  
  {{ state_attr('sensor.workout_routine', 'content') }}
```

### Updating the Content

Use the service in Developer Tools → Services:

```yaml
service: custom_markdown.update_content
target:
  entity_id: sensor.workout_routine
data:
  content: |
    # Tuesday Workout
    
    ## Warm-up
    - 5 minutes jump rope
    - Arm circles
    
    ## Main Workout
    - Deadlifts: 3 sets of 10
    - Pull-ups: 3 sets of 8
    - Planks: 3 sets of 45 seconds
  title: "Tuesday Workout"  # Optional
```

### Automation Example

```yaml
automation:
  - alias: "Daily Workout Update"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      service: custom_markdown.update_content
      target:
        entity_id: sensor.workout_routine
      data:
        content: >
          {% if now().weekday() == 0 %}
            # Monday: Chest & Triceps
            - Bench Press: 4×8
            - Incline DB Press: 3×10
            - Tricep Pushdowns: 3×12
          {% elif now().weekday() == 2 %}
            # Wednesday: Back & Biceps
            - Rows: 4×8
            - Pull-ups: 3×10
            - Bicep Curls: 3×12
          {% elif now().weekday() == 4 %}
            # Friday: Legs
            - Squats: 4×8
            - Lunges: 3×10
            - Leg Press: 3×12
          {% else %}
            # Rest Day
            Take it easy today! Do some light stretching.
          {% endif %}
        title: >
          {% if now().weekday() == 0 %}Monday Workout
          {% elif now().weekday() == 2 %}Wednesday Workout
          {% elif now().weekday() == 4 %}Friday Workout
          {% else %}Rest Day
          {% endif %}
```

## Technical Details

This integration:

- Creates a sensor entity that stores markdown content
- Persists through Home Assistant restarts
- Updates timestamps when content changes
- Registers an entity service for content updates
- Supports normal targeting for easy use in automations and scripts

## Troubleshooting

### Content Not Updating

If your content isn't updating:

1. Check that you're targeting the correct entity
2. Verify your markdown content is properly formatted
3. Look for errors in your Home Assistant logs

### Display Issues

If content isn't displaying properly:

1. Check that you're using `state_attr('sensor.your_sensor', 'content')`
2. Verify your markdown formatting is correct
3. Try a simple test content to isolate the issue

## Support & Contributing

Have ideas for improvement? Found a bug? Want to contribute?

- Open an issue on GitHub
- Submit a pull request
- Share how you're using this integration

## License

This project is licensed under MIT License - see the LICENSE file for details.

---

Enjoy your markdown! No more character limits! 🎉