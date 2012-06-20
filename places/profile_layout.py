"""Profile page visualization layout configuration.

This is where you configure what visualizations show on a profile page.
I've separated it from the view so that it's less confusing to edit later.


The profile page has visualizations organized as rows, each row
containing one or two visualizations.

Each pair of "[" abd "]," below each represent a row.

If you add a new row, be sure that each row's "]" is followed
by a comma.

Each row contains one or more Slot("xxx") objects, separated by
commas.  The xxx must exactly match the name field content of the
visualization that you want to use, which must also have its type
(called type in the admin, the model field is called kind) set to
one of "profile-table", "profile-chart", or "profile-map".

If, as with the table visualizations, you need to add text for
a heading, use Slot("xxx", title="Your Desired Title").  This
Will probably only work well on the first member of a row.
"""

from visualizations.models import Slot

LAYOUT = (

# Edit starting here

    [ Slot("health-outcomes-table", title="Health Outcomes") ],
    [ Slot("health-outcomes-chart"), Slot("health-outcomes-map") ],
    [ Slot("risk-factors-table", title="Risk Factors") ],
    [ Slot("risk-factors-chart"), Slot("risk-factors-map") ],
    [ Slot("environmant-table", title="Environment") ],
    [ Slot("environmant-chart"), Slot("environmant-map") ],
    [ Slot("social-indicators-table", title="Social Indicators") ],
    [ Slot("social-indicators-chart"), Slot("social-indicators-map") ],

# Stop editing now.
    )
