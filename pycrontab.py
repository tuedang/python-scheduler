import os
import logging
import crontab

LOG = logging.getLogger('pycrontab')


class PyCronItem(crontab.CronItem):
    def run(self):
        """Runs the given command as a pipe"""
        env = os.environ.copy()
        env.update(self.env.all())

        (out, err) = crontab.open_pipe('pythonw', *self.command.split(), env=env).communicate()
        if err:
            LOG.error(err.decode("utf-8"))
        return out.decode("utf-8").strip()


class PyCronTab(crontab.CronTab):

    def new(self, command='', comment='', user=None, pre_comment=False):
        if not user and self.user is False:
            raise ValueError("User is required for system crontabs.")
        item = PyCronItem(command, comment, user=user, cron=self, pre_comment=pre_comment)
        self.append(item)
        return item

    def __setattr__(self, name, value):
        """Catch setting crons and lines directly"""
        if name == 'lines' and value:
            for line in value:
                self.append(PyCronItem.from_line(line, cron=self), line, read=True)
        else:
            super(PyCronTab, self).__setattr__(name, value)
