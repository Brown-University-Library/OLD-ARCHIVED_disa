class Reference {

  constructor($elem, refState) {
    this._$root = $elem;
    this._$ref_id = $elem.find('.reference-id');
    this._$ref_link = $elem.find('.reference-link');
    this._$ref_edited = $elem.find('.reference-edited');
    this._$ref_delete = $elem.find('.delete-reference');
    this._$ref_cancel = $elem.find('.cancel-delete-reference');
    this._$ref_confirm = $elem.find('.confirm-delete-reference');
    
    this._$ref_id.text( refState.getId() );
    this._$ref_link.attr( 'href', refState.getLink() )
      .text( refState.getReferenceType() );
    this._$ref_edited.text( refState.getLastEdit() );
    this._$root.attr( 'data-reference-id', refState.getId() );
    this.reset();
  }

  enable() {
    this._$ref_link.addClass('disabled');
    this._$ref_cancel.removeClass('control-hide');
    this._$ref_confirm.removeClass('control-hide');
    this._$ref_delete.prop('disabled', false);
    this._$ref_delete.addClass('control-hide');
  }

  disable() {
    this._$ref_link.addClass('disabled');
    this._$ref_cancel.addClass('control-hide');
    this._$ref_confirm.addClass('control-hide');
    this._$ref_delete.prop('disabled', true);
    this._$ref_delete.removeClass('control-hide');
  }

  reset() {
    this._$ref_link.removeClass('disabled');
    this._$ref_cancel.addClass('control-hide');
    this._$ref_confirm.addClass('control-hide');
    this._$ref_delete.prop('disabled', false);
    this._$ref_delete.removeClass('control-hide');
  }

  delete() {
    this._$root.remove();
  }
}

class ReferenceControl extends Control {

  constructor($elem, urlBaseReference) {
    super()
    this._$root = $elem;
    this._$empty_display = this._$root.find('#empty_reference_display');
    this._$ref_head = this._$root.find('#reference_list_header');
    this._$ref_list = this._$root.find('#reference_list');
    this._$templates = this.getTemplates(this._$root);
    this._url_base = urlBaseReference;
    this._data = [];
    this._reference_map = {};

    this.setEvents();
  }

  load(refStateArray) {
    // this._$ref_list.empty();
    this._reference_map = {};
    for ( const refState of refStateArray ) {
      let $ref = this._$templates.reference_row.clone();
      let reference = new Reference($ref, refState);
      this._reference_map[ refState.getId() ] = reference;
      this._$ref_list.append($ref);;
    }
  }

  removeReference(refId) {
    this._reference_map[ refId ].delete();
    delete this._reference_map[ refId ];
  }

  activateReference(refId) {
    for (const mapped_id in this._reference_map) {
      if (mapped_id === refId) {
        this._reference_map[ mapped_id ].enable();
      } else {
        this._reference_map[ mapped_id ].disable();
      }
    }
  }

  show(numRefs) {
    if ( numRefs < 1 ) {
      this._$empty_display.prop('hidden', false);
      this._$ref_list.prop('hidden', true);
      this._$ref_head.prop('hidden', true);
    } else {
      this._$empty_display.prop('hidden', true);
      this._$ref_list.prop('hidden', false);
      this._$ref_head.prop('hidden', false);
    }
    this._$root.prop('hidden',false);
  }

  hide() {
    this._$root.prop('hidden',true);
  }

  activateReferences() {
    for (const mapped_id in this._reference_map) {
      this._reference_map[ mapped_id ].reset();
    }
  }

  deactivate() {
    for (const mapped_id in this._reference_map) {
      this._reference_map[ mapped_id ].disable();
    }
  }

  setEvents() {
    let cmp = this;

    this._$root.on('click', 'button', function(e){
      e.preventDefault();
      let $btn = $( this );

      switch ( true ){
        case $btn.hasClass('delete-reference'):
          cmp._app.editReference($btn.closest('.reference')
            .attr('data-reference-id'));
          break;
        case $btn.hasClass('confirm-delete-reference'):
          cmp._app.deleteReference($btn.closest('.reference')
            .attr('data-reference-id'));
          break;
        case $btn.hasClass('cancel-delete-reference'):
          cmp._app.resetReferences();
          break;
        default:
          return;
      }
    });
  }
}