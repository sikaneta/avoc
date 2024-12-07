#%%
using JSON3
using HTTP
using ProgressBars
import Base.==
#%%
ocookie = JSON3.read("C:\\Users\\ishuwa.sikaneta\\local\\src\\avoc2024.json")
resp = HTTP.request("GET", "https://adventofcode.com/2024/day/6/input", cookies=ocookie)

#%% Load data from the http response
pool = split(String(resp.body), '\n')[1:end-1]

#%% Test data
testlines = split("""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""[1:end-1], r"\n")

#%%
gridmap = pool
M = length(gridmap)
N = length(gridmap[1])

#%%
struct form
    row::Int
    col::Int
    orientation
end

#%% Overlaod the == operator so we can compare forms
==(a::form, b::form) = (a.row==b.row && 
                        a.col == b.col && 
                        a.orientation == b.orientation) ? true : false

#%%
function get_start(gridmap)
    for (row, line) ∈ enumerate(gridmap)
        for (col, element) ∈ enumerate(line)
            if element ∉ ['.', '#']
                return form(row, col, element)
            end
        end
    end
end

#%%
path = Dict('^' => (row,col) -> (row-1, col),
            '>' => (row,col) -> (row, col+1),
            'v' => (row,col) -> (row+1, col),
            '<' => (row,col) -> (row, col-1))
turn = Dict('^' => '>', '>' => 'v', 'v' => '<', '<' => '^')


#%% Let's go


function nav(f; blocker = [])
    (row,col) = path[f.orientation](f.row, f.col)
    if row == 0 || row > M || col == 0 || col > N
        return nothing
    end
    
    if gridmap[row][col] == '#' || (row,col) in blocker
        return form(f.row,f.col,turn[f.orientation])
    else
        return form(row,col,f.orientation)
    end
end

#%% generate the path
function get_path(f, block = [])
    soln = [f]
    while true
        item = nav(soln[end], blocker = block)
        if item === nothing
            break
        end
        append!(soln, [item])
        if soln[end] ∈ soln[1:end-1]
            return block[1]
        end
    end
    return soln
end

#%% Part 1
f = get_start(gridmap)
soln_path = get_path(f, [])
u_path = unique([(x.row, x.col) for x in soln_path])

part1 = length(u_path)
println("Part1: $part1")

#%%
block_path = []
for s ∈ ProgressBar(u_path[2:end])
# for s ∈ u_path[2:end]
    test = get_path(f, [s])
    if test isa Tuple
        append!(block_path, [s])
    end
end

part2 = length(unique(block_path))
println("Part2: $part2")