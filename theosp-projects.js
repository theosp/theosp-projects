(function () { 

    // load modules {{{
    var fs = require('fs'),
        populateTemplate = require('./theosp-nodejs-template-engine/template_engine').populateTemplate,
        theosp = require("./theosp_common_js/theosp"),
        spawn = require('child_process').spawn,
        exec = require('child_process').exec;
    // }}}

    // options {{{
    var options = {
        conf_file: 'project.conf',
        project_path: undefined
    };
    // }}}

    // variables {{{
    var project = null, // project is loaded in main()
        project_directory_structure = {
            javascript: {
                src: undefined
            },
            style: {
                src: undefined
            }
        },
        skeleton_templates = {
            './skeleton/style/src/base.css.less':
                'style/src/base.css.less',
            './skeleton/index.html':
                'index.html',
            './skeleton/Makefile':
                'Makefile',
            './skeleton/production_files_headers.txt':
                'production_files_headers.txt',
            './skeleton/README.rst':
                'README.rst',
            './skeleton/.gitignore':
                '.gitignore'
        },
        submodules = {
            "git@github.com:theosp/theosp_common_build_tools.git": "build",
            "git@github.com:theosp/theosp_common_js.git": "javascript/src/theosp_common_js",
            "git@github.com:theosp/theosp_common_css.git": "style/src/theosp_common_css",
            "git@github.com:theosp/headjs.git": "javascript/src/headjs"
        };
    // }}}

    // functions {{{

    // stylize (derived from lesscss's /lib/less/index.js) {{{
    function stylize(str, style) {
        var styles = {
            'bold'      : [1,  22],
            'inverse'   : [7,  27],
            'underline' : [4,  24],
            'yellow'    : [33, 39],
            'green'     : [32, 39],
            'red'       : [31, 39],
            'grey'      : [90, 39]
        };
        return '\033[' + styles[style][0] + 'm' + str +
               '\033[' + styles[style][1] + 'm';
    }
    // }}}

    // verboseExec {{{
    var verboseExec = function (command, options, callback) {
        if (typeof callback === 'undefined') {
            callback = options;
        }

        var verbosityPipe = function (error, stdout, stderr) {
            console.log(stylize("Executing Command: " + command, "yellow"));

            if (error !== null) {
                console.log([
                    stylize("\tError:", "red"),
                    JSON.stringify(error)
                        .replace(/,\"/g, ",\n\"")
                        .replace(/\\n/g, '\n')
                        .replace(/^/mg, "\t\t")
                ].join("\n"));

                console.log([
                    stylize("\tStderr:", "red"),
                    stderr.replace(/^/mg, "\t\t")
                ].join("\n"));
            }

            console.log([
                stylize("\tStdout:", "green"),
                stdout.replace(/^/mg, "\t\t")
            ].join("\n"));

            callback(error, stdout, stderr);
        };

        if (typeof options !== 'undefined') {
            return exec(command, options, verbosityPipe);
        }

        return exec(command, verbosityPipe);
    };
    // }}}

    // generate_project_leaves_directories_array {{{
    var project_leaves_directories = [],
        generate_project_leaves_directories_array = function (cwd, directory_structure) {
            for (var directory_name in directory_structure) {
                if (directory_structure.hasOwnProperty(directory_name)) {
                    if (typeof directory_structure[directory_name] !== 'undefined') {
                        generate_project_leaves_directories_array(cwd + '/' + directory_name, directory_structure[directory_name]);
                    } else {
                        project_leaves_directories.push(cwd + '/' + directory_name);
                    }
                }
            }
        };
    // }}}

    // multiple_recursive_mkdir {{{
    var multiple_recursive_mkdir = function (folders, callback) {
            var folders_count = folders.length - 1;

            for (var i = 0; i < folders.length; i++) {
                var folder = folders[i];

                (function (folder) {
                    verboseExec('mkdir -p ' + folder,
                        function () {
                            verboseExec('touch .placeholder',
                                {cwd: folder},
                                function () {
                                    folders_count -= 1;

                                    if (folders_count === 0) {
                                        callback();
                                    }
                                }
                            );
                        }
                    );
                })(folder);
            }
        };
    // }}} 

    // }}}

    // actions {{{
    var actions = {

        // help {{{
        help: function () {
            process.stdout.write([
                "NAME",
                "    theosp-projects - Initiate/Update web application projects",
                "",
                "    SYNOPSIS",
                "        ./theosp-projects [--conf=<conf-file>] [--project-path=<project-path>] [--] COMMAND <command-args>",
                "        ./theosp-projects [-h] [--help]",
                "",
                "    OPTIONS",
                "        --conf=<conf-file>",
                "            If specified, will be used instead of the default ",
                "            config file: project.conf",
                "",
                "        --project-path=<project-path>",
                "            If specified, will be used instead of the value ",
                "            stored in the project's conf file.",
                "",
                "    COMMANDS",
                "        init",
                "            Initiates new theosp project and deploy it to the",
                "            github rep set in the conf file.",
                "",
                "        update_skeleton",
                "            Render the project skeleton templates and save them",
                "            in the project directory.",
                "            The skeleton templates are listed in the",
                "            skeleton_templates object in which the keys are",
                "            the paths to templates and the values are the",
                "            place in which they should be stored in the project",
                "            repository",
                "",
                "        register_submodules",
                "            Add to the project git repository all the",
                "            submodules listed in the submodules object.",
                "",
                "        help",
                ""
            ].join("\n"));
        },
        // }}}

        // init {{{
        init: function () {
            verboseExec('mkdir ' + options.project_path,
                function () {
                    verboseExec('git init', 
                        {cwd: options.project_path},
                        function () {
                            verboseExec('touch README', 
                                {cwd: options.project_path},
                                function () {
                                    verboseExec('git add README', 
                                        {cwd: options.project_path},
                                        function () {
                                            verboseExec('git commit -m "first commit"', 
                                                {cwd: options.project_path},

                                                function () {
                                                    generate_project_leaves_directories_array(options.project_path, project_directory_structure);
                                                    multiple_recursive_mkdir(project_leaves_directories, function () {
                                                        verboseExec('git remote add origin git@github.com:' + project.github_rep + '.git', 
                                                            {cwd: options.project_path},
                                                            function () {
                                                                verboseExec('git push origin master', 
                                                                    {cwd: options.project_path},
                                                                    function () {
                                                                    }
                                                                );
                                                            }
                                                        );
                                                    });
                                                }
                                            );
                                        }
                                    );
                                }
                            );
                        }
                    );
                }
            );
        },
        // }}}

        // update_skeleton {{{
        update_skeleton: function () {
            // generate skeleton's templates components {{{
            var templates_components = {

                // Tags {{{
                tags: {
                    project_readable_name: project.readable_name
                },
                // }}}

                // Conditional sections {{{
                conditional_sections: {
                },
                // }}}

                // iterators {{{
                iterators: {
                }
                // }}}
                
            };
            // }}}

            // copy skeleton templates files to their path in the project {{{
            for (var template_path in skeleton_templates) {
                if (skeleton_templates.hasOwnProperty(template_path)) {
                    var output_path = options.project_path + '/' +
                            populateTemplate(skeleton_templates[template_path], templates_components),
                        read_stream = fs.createReadStream(template_path, {encoding: 'utf8'}),
                        write_stream = fs.createWriteStream(output_path);

                    // without a the anon func the callback for
                    // write_stream.once might hold the next for loop
                    // iteration read/write_streams
                    (function (read_stream, write_stream) {
                        var template = '';
                        read_stream
                            .on('data', function (data) {
                                template += data;
                            })
                            .on('end', function () {
                                write_stream.write(
                                    populateTemplate(template, templates_components));
                            });
                    })(read_stream, write_stream);
                }
            }
            // }}}
        },
        // }}}

        // register submodules {{{
        register_submodules: function () {
            for (var submodule in submodules) {
                if (submodules.hasOwnProperty(submodule)) {
                    var submodule_path = submodules[submodule];

                    (function (submodule, submodule_path) {
                        verboseExec('git submodule add ' + submodule + ' ' + submodule_path, 
                            {cwd: options.project_path},
                            function () { }
                        );
                    })(submodule, submodule_path);
                }
            }
        }
        // }}}

    };
    // }}}

    // getOpts {{{
    var getOpts = function (argv) {
            argv = argv.slice(2); // remove the call for node and the script name

            var action,
                action_args = [];

            // options {{{
            for (var i = 0; i < argv.length; i++) {
                var arg = argv[i];
            
                if (/^-h|--help/.test(arg)) {
                    actions.help();

                    process.exit();
                } else if (/^--conf=.+/.test(arg)) {
                    options.conf_file = arg.replace('--conf=', "");
                } else if (/^--project-path=.+/.test(arg)) {
                    options.project_path = arg.replace('--project-path=', "");
                } else if (/^--/.test(arg)) {
                    console.log("Error: Unkown option: " + arg.replace(/\=.*/, '') + "\n");
                    actions.help();

                    process.exit();
                } else {
                    // remove the options arguments from argv and exit
                    argv = argv.slice(i); 
                    break;
                }
            }
            // }}}

            // action {{{
            if (typeof argv[0] !== 'undefined') {
                action = argv[0];

                if (!(action in actions)) {
                    console.log("Error: Unknown action " + action + "." + "\n");

                    action = "help";
                }
            } else {
                console.log("Error: No action found" + "\n");

                action = "help";
            }
            // }}}

            // action_args {{{
            action_args = argv.slice(1);
            // }}}

            return {action: action, args: action_args};
        };
    // }}}

    // main {{{
    var main = function () {
        var opts = getOpts(process.argv);

        // if action isn't help {{{
        if (opts.action !== "help") {
            // normalize conf_file option {{{
            if (options.conf_file.indexOf('/') === -1) {
                options.conf_file = './' + options.conf_file;
            }
            // }}}

            // load project conf {{{
            project = require(options.conf_file).project;
            // }}}

            // if project has project_path and the user didn't explicitly set project path using command line argument option {{{
            if (typeof project.project_path !== 'undefined' && typeof options.project_path === 'undefined') {
                options.project_path = project.project_path;
            }
            // }}}

            if (typeof options.project_path === 'undefined') {
                console.log("Error: you must set your project-path either in the conf file (project_path property)");
                console.log("or by passing it as a command line argument --project-path=<project-path>\n");

                // show help and exit
                actions.help();
                process.exit();
            }

            // normalize conf_file option {{{
            if (options.project_path.slice(-1) === "/") {
                options.project_path = options.project_path.slice(0, -1);
            }
            // }}}
        }
        // }}}

        actions[opts.action].apply(this, opts.args);
    };
    // }}}

    // if main {{{
    if (!module.parent) {
        main();
    }
    // }}}

})();

// vim:ft=javascript:fdm=marker:fmr={{{,}}}:
