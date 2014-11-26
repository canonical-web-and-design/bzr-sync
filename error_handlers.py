from datetime import datetime

from sh import cat, sendmail


def email_sh_error(
    sh_error, email_dir, sender_email,
    recipient_emails, subject
):
    """
    Takes an sh.ErrorReturnCode error
    and sends an email (using sendmail) with its contents
    """

    epoch_time = datetime.now().strftime('%s')

    email_filepath = '{0}/{1}.email'.format(email_dir, epoch_time)

    with open(email_filepath, 'w') as email_file:
        email_file.write('from: {0}\n'.format(sender_email))
        email_file.write('subject: {0}\n'.format(subject))
        email_file.write('\n')
        email_file.write('{0}\n'.format(sh_error.message))
        email_file.write('\n')
        email_file.write('Exception properties\n')
        email_file.write('===\n')
        email_file.write('full_cmd: {0}\n'.format(sh_error.full_cmd))
        email_file.write('exit_code: {0}\n'.format(str(sh_error.exit_code)))
        email_file.write('stdout: {0}\n'.format(sh_error.stdout))
        email_file.write('stderr: {0}\n'.format(sh_error.stderr))

    sendmail(cat(email_filepath), recipient_emails)
