* search\_symbol.py
    * usage: search\_symbol.py [-C] word file0 [file1 ...]  

    This command execute _nm_ command to specified files and grep the _word_ from _nm_ result.
    You can specify the word in regular expression format. This tool is useful to search the library
    contains some symbol.

* cpath\_mgr
    * usage: cpath\_mgr [-a] file

    This command is the tool to manage c/c++ compilation database.
    The database file is located to ~/.compile\_commands.json and its format is clang JSON compilation database format[(http://clang.llvm.org/docs/JSONCompilationDatabase.html)](http://clang.llvm.org/docs/JSONCompilationDatabase.html).

    To add compilation data to your database, use "-a" option.

                cpath_mgr -a compile_commands.json 

    To get compilation data form your database invoke *cpath\_mgr* without "-a" option.

                cpath_mgr some_source.cpp

    This command outputs path list like below.

                .,/usr/include/c++/4.8,/usr/include/x86_64-linux-gnu/c++/4.8,/usr/include/c++/4.8/backward,/usr/lib/gcc/x86_64-linux-gnu/4.8/include,/usr/local/include,/usr/lib/gcc/x86_64-linux-gnu/4.8/include-fixed,/usr/include/x86_64-linux-gnu,/usr/include,/usr/lib/llvm-3.4/include,/include,

     This string can be set to vim variable *path* as is to be able to search c headers from *gf* command like below.

                :let &path=".,/usr/include/c++/4.8,/usr/include/x86_64-linux-gnu/c++/4.8,/usr/include/c++/4.8/backward,/usr/lib/gcc/x86_64-linux-gnu/4.8/include,/usr/local/include,/usr/lib/gcc/x86_64-linux-gnu/4.8/include-fixed,/usr/include/x86_64-linux-gnu,/usr/include,/usr/lib/llvm-3.4/include,/include,"
