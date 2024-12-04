#%%
using JSON3
using HTTP
ocookie = JSON3.read("C:\\Users\\ishuwa.sikaneta\\local\\src\\avoc2024.json")
resp = HTTP.request("GET", "https://adventofcode.com/2024/day/3/input", cookies=ocookie)

#%% Load data from the http response
pool = String(resp.body)

#%% Basic multiplication function to replicate call syntax
function mul(x,y)
    x*y
end

#%% Function to parse the string and evaluate the function
function do_it(mystr, re_str = r"mul[(][0-9]{1,3},[0-9]{1,3}[)]")
    tokens = [match.match for match in eachmatch(re_str, mystr)]
    tokens .|> Meta.parse .|> eval |> sum
end

#%% Part 1
part1 = do_it(pool)
println("Part 1: $part1")

#%% Part 2
goodstr = [split(x,r"don't[(][)]")[1] for x in split(pool,r"do[(][)]")]
part2 = goodstr .|> do_it |> sum
println("Part 2: $part2")