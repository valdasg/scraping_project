def get_salary_definition(payment_way):
    if payment_way is None:
        return
    payment_way = payment_way.lower()
    bt = ['neats','gross','pirms','before','до уплаты']
    at = ['atskaičius','net','pec','pēc','after','rankas','после уплаты','į rankas']
    for _ in bt:
        if _ in payment_way:
            payment_way = 'before tax'
    for _ in at:
        if _ in payment_way:
            payment_way = 'after tax'
    return payment_way

def get_salary(field):       
    """
    Function takes salary string field,
    and returns dictionary of numbers
    with salary from and salary to.
    Arguments:
        field: string
    Returns:
        salaries: dictionary
    """ 
    
    salaries = {
        'salary_from': 0,
        'salary_to': 0
    }
    ints = []
    if field is None:
        return salaries
    
    
    if type(field) not in [int, float]:
        for i in field:            
            i = i.strip("'")            
            try:
                i = int(i)                
                ints.append(i)
            except Exception:
                continue
    else:
        ints.append(field)
    
    if len(ints) == 1:
        salaries['salary_from'] = ints[0]
        salaries['salary_to'] = ints[0]
    elif len(ints) == 2:
        salaries['salary_from'] = ints[0]
        salaries['salary_to'] = ints[1]
    else:
        salaries['salary_from'] = 0
        salaries['salary_to'] = 0

    return salaries

def calc_nett_salary(salary, payment_way):
    """
    Function takes salary before taxes,
    and substracts all taxes
    returning nett salary after tax.
    Arguments:
        salary: float
    Returns:
        nett_salary: float
    """
    if payment_way == 'before tax':
        sodra = round(salary * 0.0698, 2)
        psd = round(salary * 0.1252, 2)

        if salary <= 1704:
            npd = round(540 - 0.34 * (salary - 730), 2)
        else:
            npd = max(round(400 - 0.18 * (salary - 730), 2), 0)
        pm = round((salary - npd) * 0.2, 2)
        nett_salary = round((salary - pm - sodra - psd), 2)
        return nett_salary
    else:
        return salary


    
    
    
    

        
    
    

