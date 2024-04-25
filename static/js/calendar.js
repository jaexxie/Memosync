document.addEventListener('DOMContentLoaded', function() {

      // popup
      add_event_btn = document.querySelector('#add_event_btn')
      background_create_event = document.querySelector('.background_create_event')
      container_create_event = document.querySelector('.container_create_event')
      background_view_event = document.querySelector('.background_view_event')
      container_view_event = document.querySelector('.container_view_event')
      paragraphs = document.querySelectorAll('#event_info')

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
      paragraphs[0].innerText =  'Event Name: ' + info.event.title
      paragraphs[2].innerHTML = '<a href="delete/event/' + info.event.id + '" id="delete_event_link">Delete Event</a>';
      // change the border color just for fun
      info.el.style.border = '1.5px solid #2c3e50';
    }

      });
      calendar.render();
    });