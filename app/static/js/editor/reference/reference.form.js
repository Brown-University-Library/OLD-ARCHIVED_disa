class AutoCompleteInput {

  constructor($input) {
    this._$input = $input;
    this._auto_data = [];
    this._value = '';
    this._value_id = '';
  }

  setAutoComplete(autoCompleteValues, settings) {
    let cmpt = this;
    for (var i=0; i < autoCompleteValues.length; i++) {
      var acObj = autoCompleteValues[i];
      this._auto_data.push({
        'id': acObj.id,
        'value': acObj.name,
        'label': acObj.name
      })
    }

    this._$input.autocomplete({
        source: cmpt._auto_data,
        minLength: settings.minLength,
        delay: settings.delay,
        autoFocus: settings.autoFocus,
        response: function (event, ui) {
          if (ui.content.length == 0) {
            ui.content.push({
              label: cmpt._$input.val(),
              value: cmpt._$input.val(),
              id: 'new'
            });
          }
        },
        change: function (event, ui) {
          let data = { 'id': '', 'name': ''};
          if (ui.item) {
            data.id = ui.item.id;
            data.name = ui.item.value;
          }
          cmpt.load(data);
        }
    });
  }

  load(data) {
    this._value = data.name;
    this._value_id = data.id;
    this._$input.val(data.name);
  }

  isEmpty() {
    return this._value === '';
  }

  read() {
    return { 'id': this._value_id, 'name': this._value } ;
  }
}

class RichTextInput {

  constructor($elem) {
    this._$input = $elem;
    this._id = $elem.attr('id');
    this._settings = {};
  }

  setEditor(settings) {
    settings.selector = `#${this._id}`;
    this._settings = settings;
  }

  load(data) {
    if (!tinymce.get(this._id)) {
      let cmpt = this;
      tinymce.init(this._settings)
        .then(function(editors) {
          cmpt._$input.val(data);
          tinymce.get(cmpt._id).load();
        });
    } else {
      this._$input.val(data);
      tinymce.get(this._id).load();
    }
  }

  read(data) {
    tinymce.triggerSave();
    return this._$input.val();
  }
}

class LocationField extends AutoCompleteInput {

  constructor($elem) {
    super($elem);
    this._$root = $elem;
    this._location_type_id = '';
  }

  getType() {
    return this._location_type_id;
  }

  setType(val) {
    this._location_type_id = val;
  }

  read() {
    let data = super.read();
    data.location_type_id = this._location_type_id;
    return data;
  }
}

class DateSelect {

  constructor($elem) {
    this._$root = $elem;
    this._$day = $elem.find('#date_day');
    this._$month = $elem.find('#date_month');
    this._$year = $elem.find('#date_year');
    this._$text = $elem.find('#date_text');
  }

  read() {
    return {
      'day': this._$day.val(),
      'month': this._$month.val(),
      'year': this._$year.val(),
      'text': this._$text.val()
    }
  }

  load(data) {
    this._$day.val(data.day);
    this._$month.val(data.month);
    this._$year.val(data.year);
    this._$text.val(data.text);
  }
}

class ReferenceForm extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._$discard_btn = $elem.find('.discard-new-reference');
    this._$cancel_btn = $elem.find('.cancel-edit-reference');

    this._data = {};
    this._locations_by_type = {};

    this._ref_type = new AutoCompleteInput($elem.find('#reference_type_input'));
    this._col_state = new LocationField($elem.find('#colony_state_input'));
    this._city = new LocationField($elem.find('#city_input'));
    this._locale = new LocationField($elem.find('#locale_input'));
    this._date = new DateSelect($elem.find('#date_selector'));
    this._trsc = new RichTextInput($elem.find('#transcription_input'));

    this.setEvents();
  }

  configure(config, autoCmplSettings, richTextSettings) {
    this._trsc.setEditor(richTextSettings);

    this._ref_type.setAutoComplete(config.get('reference_types'),
      autoCmplSettings);

    let loc_type_map = config.get('location_types');
    this._col_state.setAutoComplete(config.get('colony_states'),
      autoCmplSettings);
    this._col_state.setType(loc_type_map['Colony/State']);    
    this._city.setAutoComplete(config.get('cities'),
      autoCmplSettings);
    this._city.setType(loc_type_map['City']);
    this._locale.setAutoComplete(config.get('locales'),
      autoCmplSettings);
    this._locale.setType(loc_type_map['Locale']);

    this._locations = [ this._col_state, this._city, this._locale ];
    for (var i=0; i < this._locations.length; i++) {
      let loc_field = this._locations[i];
      this._locations_by_type[ loc_field.getType() ] = loc_field;
    }
  }

  load(data) {
    this._data = data;
    this._ref_type.load(data.reference_type);
    for (var i=0; i < data.locations.length; i++) {
      let loc = data.locations[i];
      this._locations_by_type[ loc.type ].load(loc);
    }
    this._date.load(data.date);
    this._trsc.load(data.transcription);
  }

  read() {
    this._data.locations = []
    for (var i=0; i < this._locations.length; i++) {
      let loc = this._locations[i];
      if (!loc.isEmpty()) {
        this._data.locations.push(loc.read());
      }
    }
    this._data.reference_type = this._ref_type.read();
    this._data.date = this._date.read();
    this._data.transcription = this._trsc.read();
    return this._data;
  }

  activate() {
    if (this._data.reference_id === 'new') {
      this._$discard_btn.removeClass('hidden');
      this._$cancel_btn.addClass('hidden');
    } else {
      this._$discard_btn.addClass('hidden');
      this._$cancel_btn.removeClass('hidden');
    }
    this._$root.removeClass('hidden');
  }

  deactivate() {
    this._$root.addClass('hidden');
  }

  reset() {
    this.load(this._data);
    this.deactivate();
  }

  setEvents() {
    let cmp = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('save-reference'):
          cmp._app.saveReference();
          break;
        case $btn.hasClass('cancel-edit-reference'):
          cmp._app.resetReference();
          break;
        default:
          return;
      }
    });
  }
}