class TagSelector {

  constructor($select, settings) {
    this._$select = $select;
    this._$select.attr("multiple", true);
    this._$select.select2(settings);
  }

  load(data) {
    this._$select.val(data);
    this._$select.trigger('change');
  }

  isEmpty() {
    return this._$select.val === [];
  }

  read() {
    return this._$select.val();
  }

  clear() {
    this.load([]);
  }
}

class ReferentRow {

  constructor($elem, tagSettings) {
    this._$root = $elem;
    this._$rnt_id = $elem.find('.referent-id');
    this._$rnt_first_ = $elem.find('.referent-first');
    this._$rnt_last = $elem.find('.referent-last');
    this._$rnt_tags = new TagSelector( $elem.find('.referent-tags'),
      tagSettings );
    this._$rnt_details = $elem.find('.referent-details');
    this._$rnt_edit = $elem.find('.edit-referent');
    this._$rnt_save = $elem.find('.save-referent');
    this._$rnt_delete = $elem.find('.delete-referent');
    this._$rnt_cancel = $elem.find('.cancel-edit-referent');
    this._$rnt_confirm = $elem.find('.confirm-delete-referent');
  }

  load(rntState) {
    this._$root.attr( 'data-referent-id', refState.getId() );
    this._$rnt_id.text( rntState.getId() );
    this._$rnt_first.val( rntState.getFirstName() );
    this._$rnt_last.val( rntState.getLastName() );
    this._$rnt_tags.load( rntState.getTags() );
    this._$rnt_details.attr( 'href', rntState.getDetailsLink() );
  }

  enable() {
    this._$rnt_first.prop('disabled', false);
    this._$rnt_last.prop('disabled', false);
    this._$rnt_tags.prop('disabled', false);
    this._$rnt_cancel.removeClass('hidden');
    this._$rnt_save.removeClass('hidden');
    this._$rnt_delete.removeClass('hidden');
    this._$rnt_edit.addClass('hidden');
    this._$rnt_details.addClass('hidden');
  }

  confirmDelete() {
    this._$rnt_first.prop('disabled', true);
    this._$rnt_last.prop('disabled', true);
    this._$rnt_tags.prop('disabled', true);
    this._$rnt_cancel.removeClass('hidden');
    this._$rnt_confirm.removeClass('hidden');
    this._$rnt_edit.addClass('hidden');
    this._$rnt_details.addClass('hidden');
  }

  disable() {
    this._$rnt_first.prop('disabled', true);
    this._$rnt_last.prop('disabled', true);
    this._$rnt_tags.prop('disabled', true);
    this._$rnt_cancel.addClass('hidden');
    this._$rnt_save.addClass('hidden');
    this._$rnt_delete.addClass('hidden');
    this._$rnt_confirm.addClass('hidden');
    this._$rnt_edit.removeClass('hidden');
    this._$rnt_details.removeClass('hidden');
  }

  reset() {
    this._$rnt_first.prop('disabled', true);
    this._$rnt_last.prop('disabled', true);
    this._$rnt_tags.prop('disabled', true);
    this._$rnt_cancel.addClass('hidden');
    this._$rnt_save.addClass('hidden');
    this._$rnt_delete.addClass('hidden');
    this._$rnt_confirm.addClass('hidden');
  }

  delete() {
    this._$root.remove();
  }
}

class ReferentControl extends Control {

  constructor($elem) {
    super()
    this._$root = $elem;
    this._$empty_display = this._$root.find('#empty_referent_display');
    this._$rnt_head = this._$root.find('#referent_list_header');
    this._$rnt_list = this._$root.find('#referent_list');
    this._$templates = this.getTemplates(this._$root);
    this._referent_map = {};
    this._tag_options = [];
    this._tag_settings = {};

    this.setEvents();
  }

  configure(config, tagConfig) {
    this._tag_options = config.referent_tags;
    this._tag_settings = tagConfig;
  }

  load(rntStateArray) {
    this._$rnt_list.empty();
    this._referent_map = {};
    for ( const rntState of rntStateArray ) {
      let $rnt = this._$templates.referent_row.clone();
      let rnt_row = new ReferentRow($rnt, this._tag_settings);
      rnt_row.load( rntState );
      rnt_row.reset();
      this._referent_map[ rntState.getId() ] = rnt_row;
      this._$rnt_list.append($rnt);
    }
  }

  updateReferent(rntState) {
    this._referent_map[ rntState.getId() ].load(rntState);
  }

  removeReferent(refId) {
    this._referent_map[ refId ].delete();
    delete this._referent_map[ refId ];
  }

  activateReferent(rntId) {
    for (const mapped_id in this._referent_map) {
      if (mapped_id === rntId) {
        this._referent_map[ mapped_id ].enable();
      } else {
        this._referent_map[ mapped_id ].disable();
      }
    }
  }

  show(numRnts) {
    if ( numRnts < 1 ) {
      this._$empty_display.prop('hidden', false);
      this._$rnt_list.prop('hidden', true);
      this._$rnt_head.prop('hidden', true);
    } else {
      this._$empty_display.prop('hidden', true);
      this._$rnt_list.prop('hidden', false);
      this._$rnt_head.prop('hidden', false);
    }
    this._$root.prop('hidden',false);
  }

  hide() {
    this._$root.prop('hidden',true);
  }

  resetReferents() {
    for (const mapped_id in this._referent_map) {
      this._referent_map[ mapped_id ].reset();
    }
  }

  deactivate() {
    for (const mapped_id in this._referent_map) {
      this._referent_map[ mapped_id ].disable();
    }
  }

  setEvents() {
    let cmp = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('delete-referent'):
          cmp._app.editReferent($btn.closest('.referent-row')
            .attr('data-referent-id'));
          break;
        case $btn.hasClass('confirm-delete-referent'):
          cmp._app.deleteReferent($btn.closest('.referent-row')
            .attr('data-referent-id'));
          break;
        case $btn.hasClass('cancel-delete-referent'):
          cmp._app.resetReferents();
          break;
        default:
          return;
      }
    });
  }
}