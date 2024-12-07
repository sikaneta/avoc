#%%
using JSON3
using HTTP
using Combinatorics

#%%
ocookie = JSON3.read("C:\\Users\\ishuwa.sikaneta\\local\\src\\avoc2024.json")
resp = HTTP.request("GET", "https://adventofcode.com/2024/day/4/input", cookies=ocookie)

#%% Load data from the http response
pool = String(resp.body)

#%% Test data
rules, lines = split("""
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""[2:end-1], r"\n\n")

#%%
rules = split(rules, '\n')
lines = map(x->split(x,','), split(lines, '\n'))

#%% Check whether a line is valid
function checkline(line, rules)
    for x ∈ combinations(line,2)
        if join(reverse(x), "|") ∈ rules
            return false
        end
    end
    return true
end

#%%
mid(x) = parse(Int, x[1+Int(trunc(length(x)/2))])

#%%
function reorder(line, rules)
    for k ∈ combinations(1:length(line),2)
        if join(reverse(k) .|> idx -> line[idx], "|") ∈ rules
            return false
        end
    end
    return true
end

#%% Part 1
part1 = lines .|> (x -> checkline(x,rules) ? mid(x) : 0) |> sum
println("Part 1: $part1")

#%% Part 2
goodstr = [split(x,r"don't[(][)]")[1] for x in split(pool,r"do[(][)]")]
part2 = goodstr .|> do_it |> sum
println("Part 2: $part2")