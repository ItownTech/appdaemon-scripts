import appdaemon.plugins.hass.hassapi as hass
import messages
import globals
#
# App to send notification when a login attemp fails
#
# Args:
#  notify_name: who to notifiy
#
# Release Notes
#
# Version 1.1:
#   Using globals now
#
# Version 1.0:
#   Initial Version

class NotifyFailedLogin(hass.Hass):

  def initialize(self):

    self.timer_handle_list = []
    self.listen_event_handle_list = []
    self.listen_state_handle_list = []


    self.notify_name = globals.get_arg(self.args,"notify_name")
    
    self.listen_state_handle_list.append(self.listen_state(self.state_change, "persistent_notification.httplogin"))
    
  def state_change(self, entity, attribute, old, new, kwargs):
    if new != "" and new == "notifying":
        message = self.get_state("persistent_notification.httplogin",attribute="message")
        self.log(message)
        self.call_service("notify/" + self.notify_name,message=messages.failed_login_detected().format(message))

  def terminate(self):
    for timer_handle in self.timer_handle_list:
      self.cancel_timer(timer_handle)

    for listen_event_handle in self.listen_event_handle_list:
      self.cancel_listen_event(listen_event_handle)

    for listen_state_handle in self.listen_state_handle_list:
      self.cancel_listen_state(listen_state_handle)
      