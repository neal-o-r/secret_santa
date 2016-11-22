import random as rd
import smtplib

with open('people.txt', 'r') as f:
	txt = f.readlines()

receivers = txt[0].strip().split(',')

givers = list(receivers)

emails = txt[1].strip().split(',')

def make_pairs(n):
	# this function returns a tuple,
	# containing two lists of indices
	# these are a random derangement of the inds from 0->n

	give_no = range(n)
	rec_no  = range(n)
	inds = range(n)
	rd.shuffle(inds)
	
	# if you have a lot of friends then the O(n) of this 
	# might be a bottle-neck and require vectorising. 
	# I don't.
	give_no = [give_no[i] for i in inds] 
	rec_no  = [rec_no[i] for i in inds]
	
	# roll the givers by one
	give_no = [give_no[-1]] + give_no[:-1] 

	return give_no, rec_no	


def email(givers, receivers, emails):

	g_ind, r_ind = make_pairs(len(givers))

	for g, r in zip(g_ind, r_ind):

		gifter  = givers[g]
		giftee  = receivers[r]
		address = emails[g]

    		server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    		gmail_user = "email address"
    		gmail_pwd = "password"
    		server.login(gmail_user,gmail_pwd)

		FROM = ''
    		TO = [address] #must be a list
    		SUBJECT = "From Santa"

		with open('message.txt', 'r') as f:
			txt = f.read()
		
		TEXT = txt.replace('NAME', gifter).replace('GIFTEE', giftee)

        	# Prepare actual message
    		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (
                        FROM, ", ".join(TO), SUBJECT, TEXT)
    
    		try:
        		server = smtplib.SMTP("smtp.gmail.com", 587) #port 465 doesn't seem to work!
        		server.ehlo()
        		server.starttls()
        		server.login(gmail_user, gmail_pwd)
        		server.sendmail(FROM, TO, message)
        		server.close()
        		print 'successfully sent the mail'
    		except:
        		print "failed to send mail"


if __name__ == '__main__':
	email(givers, receivers, emails)


