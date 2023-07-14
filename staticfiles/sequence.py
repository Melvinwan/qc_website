# list_a = [[2,5,7,16],[1,4,8,12]]
# length=[[2,1,5,5],[2,3,3,5]]

# # input in nanoseconds and convert to clock ticks

# # list_a = [[2,5,7,16],[2,5,7,16]]
# # length=[[2,1,5,5],[2,1,5,5]]

def sequence_TTL(list_a, length,pins):
    """
    The function `sequence_TTL` takes in a list of lists, a list of lengths, and a list of pins, and
    returns a tuple containing a new list of values, a new list of lengths, and a list of pins.
    @param list_a - The parameter `list_a` is a list of lists. Each inner list represents a sequence of
    values.
    @param length - The "length" parameter is a list of lists. Each inner list represents the lengths of
    the sublists in "list_a". The lengths in each inner list correspond to the elements in the same
    position in "list_a".
    @param pins - The `pins` parameter is a list that contains the pin numbers associated with each
    sublist in `list_a`. Each sublist represents a sequence of values. The `pins` list should have the
    same length as `list_a`, and each element in `pins` corresponds to the pin number for the
    corresponding
    @returns a tuple containing three lists: `new_list_a`, `new_length`, and `pins_seq`.
    """

    end_list = []

    for ii, sub_list in enumerate(list_a):
        temp_list = []
        for cc, val in enumerate(sub_list):
            temp_list.append(val+length[ii][cc])
        end_list.append(temp_list)

    flat_list = [element for innerList in list_a+end_list for element in innerList]

    unique_list = list(set(flat_list))
    unique_list.sort()

    indexa = [i*0 for i in range(len(list_a))]

    new_list_a = []
    new_length = []
    pins_seq = []

    for k in range(len(unique_list)-1):
        temp = []
        for i in range(len(list_a)):
            if indexa[i]< len(list_a[i]):
                if unique_list[k]>=list_a[i][indexa[i]]:
                    if unique_list[k]<end_list[i][indexa[i]]:
                        if unique_list[k] not in new_list_a:
                            new_list_a.append(unique_list[k])
                            new_length.append(unique_list[k+1]-unique_list[k])
                        temp.append(pins[i])
                    else:
                        indexa[i] += 1
        if len(temp)!=0:
            temp.sort()
            pins_seq.append(temp)

    return (new_list_a,new_length,pins_seq)
# # print(unique_list)
# print(new_list_a)
# print(new_length)
# print(pins_seq)

# time = [[2,5,7,16],[1,4,8,12]]
# length=[[2,1,5,5],[2,1,5,5]]

# length=[[200,200,200,200],[200,200,200,200],[200,200,200,200],[200,200,200,200]] # [Clock ticks]
# time=[[0,300,600,1000],[0,400,700,950],[0,300,800,1300],[0,300,600,1100]]
# pins = [3,0,1,2]
# print(sequence_TTL(time, length,pins))
