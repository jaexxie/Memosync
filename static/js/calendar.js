document.addEventListener('DOMContentLoaded', function() {

  // popup
  add_event_btn = document.querySelector('#add_event_btn')
  background_create_event = document.querySelector('.background_create_event')
  container_create_event = document.querySelector('.container_create_event')
  background_view_event = document.querySelector('.background_view_event')
  container_view_event = document.querySelector('.container_view_event')
  closeBtn = document.querySelector(".close")
  closeBtn_2 = document.querySelector(".close_2");

  add_event_btn.addEventListener('click', function() {
    background_create_event.classList.add('show')
    container_create_event.classList.add('show')
  });

  background_create_event.addEventListener("click", function() {
    background_create_event.classList.remove('show')
    container_create_event.classList.remove('show')
  });

  background_view_event.addEventListener("click", function() {
    background_view_event.classList.remove('show')
    container_view_event.classList.remove('show')
  });

  closeBtn.addEventListener('click', function() {
    background_create_event.classList.remove('show')
    container_create_event.classList.remove('show')
  });

  closeBtn_2.addEventListener('click', function() {
    background_view_event.classList.remove('show')
    container_view_event.classList.remove('show')
  });

  // this creates a default datestamp for the input valeus
  var currentDate = new Date().toISOString().split('T')[0];
  document.getElementById('start_date').value = currentDate;
  document.getElementById('end_date').value = currentDate;

  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {

    // this code shows the diffrent views
    initialView: 'timeGridWeek',
    headerToolbar: {
      left: 'prev,next',
      center: 'title',
      right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,listWeek' // user can switch between the two
    },

    // You can select days with selectable true
    selectable: true,

    eventSources: [

    // your event source
    {
      url: '/get_events', // use the `url` property
      color: '#A63A50',    // an option!
      textColor: 'white'  // an option!
    }

  ],

  eventClick: function(info) {
    background_view_event.classList.add('show')
    container_view_event.classList.add('show')

    title = document.querySelector('#title')
    description = document.querySelector('#description')
    start_date = document.querySelector('#start_date_edit')
    end_date = document.querySelector('#end_date_edit')
    start_time = document.querySelector('#start_time_edit')
    end_time = document.querySelector('#end_time_edit')
    edit_event_id = document.querySelector('#edit_event_id')
    delete_event = document.querySelector('#delete_event')
    

    // Extracting event data
    const event = info.event;
    const eventStart = new Date(event.start);
    const eventEnd = new Date(event.end);

    // Updating HTML elements with event data
    edit_event_id.value = event.id;
    title.value = event.title;

    if (event.extendedProps.description) {
      description.value = event.extendedProps.description;
    } else {
        console.warn('Event description is undefined');
        description.value = '';
    }

    start_date.value = eventStart.toISOString().substring(0, 10);
    end_date.value = eventEnd.toISOString().substring(0, 10);
    start_time.value = eventStart.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    end_time.value = eventEnd.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
    
    delete_event.innerHTML = '<a href="delete/event/' + info.event.id + '" id="delete_event_link">Delete Event</a>';
    // change the border color just for fun
    info.el.style.border = '1.5px solid #2c3e50';
  },

  });
  calendar.render();
});