# Watch statics and automatically run build tasks
#
# Run me with:
#    $ watchr static.watchr
#
# More info about watchr:
#    https://github.com/mynyml/watchr/

require 'logger'
require 'systemu'

@log = Logger.new(STDOUT)
@log.level = Logger::INFO
@log.datetime_format = "%b %d %H:%M:%S"
@log.formatter = proc do |severity, datetime, progname, msg|
    "#{datetime} [BTCx Watchr]: #{msg}\n"
end

# --------------------------------------------------
# Rules
# --------------------------------------------------

# base
watch( 'btcx/static/btcx/(.*)\.less' ) { |m| compile_less(m[0]) }
watch( 'btcx/static/btcx/(.*)\.js'   ) { |m| collectstatic }
watch( 'btcx/static/btcx/(.*)\.css'  ) { |m| collectstatic }

# all other apps
watch( 'btcx/apps/(.*)\.less' ) { |m| compile_less(m[0]) }
watch( 'btcx/apps/(.*)\.js'   )  { |m| collectstatic }
watch( 'btcx/apps/(.*)\.css'   ) { |m| collectstatic }


# --------------------------------------------------
# Signal Handling
# --------------------------------------------------

Signal.trap('QUIT') { abort("echo goodbye\n") } # Ctrl-\$
Signal.trap('INT' ) { abort("\n") } # Ctrl-C


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def notify(message)
    system "growlnotify -t 'BTCx lessc' -m '#{message}'"
    @log.info("Notification sent: #{message}")
end

def collectstatic()
    @log.info("Collecting static")
    status, stdout, stderr = systemu "/Users/evanculver/.virtualenvs/btcx/bin/python manage.py collectstatic --noinput"

    message = if status == 0
            stdout.gsub!(/\n/, "")
        else
            "Could not collect static: #{stderr}"
        end

    @log.info(message)
    notify message
end

def compile_less(path)
    @log.info("Compiling #{path}")
    basename = File.basename(path, '.*')
    dirname = File.dirname(path)
    status, stdout, stderr = systemu "lessc #{path} > #{dirname}/../css/#{basename}.css"

    message = if status == 0
            "Successfully built #{path}"
        else
            "Build failed for #{path}"
        end

    @log.info(message)
    notify message
end
