# django
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# utiltities
import threading


class EmailThread(threading.Thread):
	"""
	Class uses a thread to send email
	"""
	def __init__(self, subject, content, recipient_list, is_html):
		self.subject = subject
		self.recipient_list = recipient_list
		self.content = content
		self.is_html = is_html
		threading.Thread.__init__(self)

	def run (self):
		msg = EmailMessage(
			self.subject,
			self.content,
			settings.DEFAULT_FROM_EMAIL,
			self.recipient_list
		)
		if self.is_html:
			msg.content_subtype = "html"
		msg.send()


def send_mail(subject, content, recipients, is_html=False):
	"""
	Sends email using EmailThread class
	"""
	EmailThread(subject, content, recipients, is_html).start()


def send_template_mail(subject, template_name, context, recipients, is_html):
	"""
	Send email using EmailThread class with a template
	"""
	if len(recipients) == 0:
		return None
	content = render_to_string(template_name, context)
	send_mail(subject, content, recipients, is_html)


def send_html_template_mail(subject, template_name, context, recipients):
	"""
	Send email using EmailThread class with a html template
	"""
	send_template_mail(subject, template_name, context, recipients, True)


def send_text_template_mail(subject, template_name, context, recipients):
	"""
	Send email using EmailThread class with a plain text template
	"""
	send_template_mail(subject, template_name, context, recipients, False)


