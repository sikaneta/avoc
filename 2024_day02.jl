#%%
using JSON3
using HTTP
ocookie = JSON3.read("C:\\Users\\ishuwa.sikaneta\\local\\src\\avoc2024.json")
resp = HTTP.request("GET", "https://adventofcode.com/2024/day/2/input", cookies=ocookie)

#%% Load data from the http response
pool = split(String(resp.body),"\n")
myarr = [split(p, " ") .|> (x -> parse(Int, x)) for p in pool[1:end-1]]

#%% Basic multiplication function to replicate call syntax
function bounds∇(x)
    ∇x = diff(x)
    (minimum(∇x), maximum(∇x))
end

#%% Function to parse the string and evaluate the function
function admit(x)
    Int((x[1] >= -3 & x[2] <=-1) | (x[1] >= 1 & x[2] <=3))
end

#%% Part 1
println("Part 1: $(myarr .|> bounds∇ .|> admit |> sum)")
