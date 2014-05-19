#include <pebble.h>

Window *window;	
static TextLayer *text_layer;
static char pc[10];

// Key values for AppMessage Dictionary
enum {
  QUOTE_KEY_PC = 1
};

// Write message to buffer & send
void send_message(void){
	DictionaryIterator *iter;
	
	app_message_outbox_begin(&iter);

	//dict_write_uint8(iter, STATUS_KEY, 0x1);
	//dict_write_end(iter);
	 Tuplet value = TupletCString(1, "NEXT");
 	 dict_write_tuplet(iter, &value);
  	app_message_outbox_send();
}


 void out_sent_handler(DictionaryIterator *sent, void *context) {
   // outgoing message was delivered
 }


 void out_failed_handler(DictionaryIterator *failed, AppMessageResult reason, void *context) {
   // outgoing message failed
 }


 void in_received_handler(DictionaryIterator *iter, void *context) {
   // incoming message received
	
	      //text_layer_set_text(text_layer, received);	
	       // Check for fields you expect to receive ??????
         Tuple *text_tuple = dict_find(iter, QUOTE_KEY_PC);

         // Act on the found fields received
         if (text_tuple) {
            strncpy(pc,  text_tuple->value->cstring, 10);
            text_layer_set_text(text_layer, pc);
  }
 }


 void in_dropped_handler(AppMessageResult reason, void *context) {
   // incoming message dropped
 }

static void down_click_handler(ClickRecognizerRef recognizer, void *context) {
  text_layer_set_text(text_layer, "Down");
  send_message();
  
}

static void click_config_provider(void *context) {
  //window_single_click_subscribe(BUTTON_ID_SELECT, select_click_handler);
  //window_single_click_subscribe(BUTTON_ID_UP, up_click_handler);
  window_single_click_subscribe(BUTTON_ID_DOWN, down_click_handler);
}
void init(void) {
	window = window_create();
	window_stack_push(window, true);
	
	// Register AppMessage handlers
	app_message_register_inbox_received(in_received_handler); 
	app_message_register_inbox_dropped(in_dropped_handler); 
	app_message_register_outbox_failed(out_failed_handler);
	app_message_register_outbox_sent(out_sent_handler);
		
	app_message_open(app_message_inbox_size_maximum(), app_message_outbox_size_maximum());
	
	send_message();
  
 	window_set_click_config_provider(window,click_config_provider);
}

void deinit(void) {
	app_message_deregister_callbacks();
	window_destroy(window);
}


int main( void ) {
	init();
  text_layer_set_text(text_layer, "Press DOWN button for next!");
  text_layer_set_text_alignment(text_layer, GTextAlignmentCenter);
  
	app_event_loop();
  
  
	deinit();
}
