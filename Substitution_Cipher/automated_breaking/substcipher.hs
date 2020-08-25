-- Abhyuday Pandey (170039)
import Data.List
import Data.Function
import System.Random
import Data.Maybe (fromMaybe)
import qualified Data.Map as M

removeWhite :: String -> String
removeWhite xs = [ x | x <- xs, not (x `elem` " ,.\n'\"") ]

reverseList :: [a]->[a]
reverseList [] = []
reverseList (x:xs) = reverseList xs ++ [x]


countCharacters :: String -> [(Char,Int)]
countCharacters str = reverseList $sortBy (compare `on` snd) $ map ( \x -> (head x, length x) ) $ group $ sort $removeWhite str

checkIfElem ::  [(String)]-> String -> Bool
checkIfElem dict str = if str `elem` dict then True else False

wordCount :: [(String)] -> [(String)] -> Int
wordCount [] dict = 0
wordCount str dict =  foldl (\acc x -> if (checkIfElem dict x) then acc+1 else (acc))  0 str

search :: [(Char,Char)] -> Char -> Char
search hmap '.' = '.'
search hmap ' ' = ' '
search hmap '\n' = '\n'
search [] p = p
search (x:xs) p
    | fst (x) == p = snd(x)
    | otherwise = search (xs) p

replace :: String -> [(Char,Char)] -> String
replace [] hmap = []
replace str hmap = map (\x-> search hmap x) str

substitute :: [(String)] -> [(Char,Char)] -> [(String)]
substitute [] hmap = []
substitute str hmap = map (\x -> replace x hmap) str

init_guess :: [(Char, Int)] -> [(Char, Char)]
--Replaces symbols with alphabets
init_guess x = map (\i -> ((fst (x !! i)), (freq_table !! i))) [0..(min 25 ((length x) - 1))] 
               where freq_table = ['e','a','w','i','o','t','n','s','l','c','u','d','p','m','h','g','b','f','y','r','k','v','x','z','j','q']

fitness :: [String]->[String]->[(Char,Char)]->Int
--fitness score of string
fitness str dict hmap = wordCount (substitute str hmap) dict

rand_swap :: [(Char, Char)] -> Int -> Int -> [(Char, Char)]
rand_swap x a b = map (\i -> if ((i == a) || (i == b)) then ((fst (x !! i)), (snd (x !! (a+b-i)))) else (x !! i)) [0..((length x)-1)]

nPseudorandomNumbers :: Int -> Int -> [Int]
nPseudorandomNumbers seed a = take 8000 . randomRs (0, a) . mkStdGen $ seed

incr_fit :: [String] -> [String] -> [(Char, Char)] -> Int -> Int -> [(Char, Char)]
--[words], dict, initial_map, a, b, swapped_map
incr_fit w d mi a b = if ((fitness w d (rand_swap mi a b)) > (fitness w d mi)) then (rand_swap mi a b) else mi

iterates :: [String] -> [String] -> [(Char,Char)] -> [Int] -> Int -> [(Char,Char)]
iterates w dict hmap randNums 8000 = hmap
iterates w dict hmap randNums i = iterates w dict (incr_fit w dict hmap (randNums !! i) (randNums !! (i+1)) ) randNums (i+2)


main :: IO ()
main =  do
    buffer <- readFile("wor.txt")
    let dict = sort(words buffer)
    str <- readFile("cipher.txt") :: IO String
    let hmap = init_guess (countCharacters str)
    print(fitness (words (str)) dict hmap)
    let randNums = nPseudorandomNumbers 0 ((length hmap) - 1)
    let hmap1 = iterates (words (str)) dict hmap randNums 0
    print(fitness (words str) dict hmap1)
    print(replace (str) hmap1)
