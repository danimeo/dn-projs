using Distributed

function fm(lang::String="en")
    d_dicts = Dict{String, List{String}}()

    println("Welcome to FM! Language has been set to " * lang * ".")

    """f_dict = open("OALD8EnCh_tabfile_3.txt")

    lines = readlines(f_dict)

    run(`echo -e "\033[47m\033[2J"`)
    while true
        run(`echo -e "\033[47;30m请输入单词："`)
    
        word  = readline(stdin)
        if isempty(word)
            continue
        elseif word == "="
        run(`echo -e "\033[0m"`)
        break
        end

        exp = ""
        for line = lines
            w_n_e = split(line, '\t')
            if w_n_e[1] == word
                exp = w_n_e[2]
                break
            end
        end

        str_prom1 = "\n已输入单词：" * word
        str_prom2 =  "\n"
        str_exp = exp
        str_sep = "\n\n========================================================="
        run(`echo -e "\033[42;37m$str_prom1\033[47m$str_prom2\033[47;30m$str_exp\033[47;32m$str_sep"`)
        println()
    end"""

end

