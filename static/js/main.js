// ADD ALL IMPORTS FOR PLUGINS HERE
import { updateClock } from './plugins/clock_script.js';
import {} from './plugins/temperature_script.js'
import {} from './plugins/weather_script.js'
import {} from './plugins/timeZone_script.js'
import {} from './plugins/date_script.js';
import {} from './plugins/tasks_script.js'
import './plugins/spotify_script.js';           
import { updateCalendar } from './plugins/calendar_script.js';
import { updatePackages } from './plugins/package_script.js';
import {updateArrivingToday} from './plugins/arrivingToday_script.js'

// Call update functions for each plugin
updateClock();
updateCalendar();
updatePackages();
import './plugins/fakeLight_script.js';

import './plugins/blackjack_script.js'





function getActiveClientId() {
    return localStorage.getItem('client_id') || 'default_client';
}

