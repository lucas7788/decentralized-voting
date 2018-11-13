"""
A sample of OEP5 smart contract
"""
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import CheckWitness, Notify, Serialize, Deserialize
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash
from boa.builtins import ToScriptHash, sha256, concat

# modify to the admin address
admin = ToScriptHash('AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p')

# 举办选举活动
KEY_VOTE_ACTION = 'VoteAction'

# 候选人
KEY_CANDIDATE = 'Candidate' # 候选人
KEY_CANDIDATE_APPLY = 'Applier' # 申请人
KEY_POLL = 'Poll' # 票数
KEY_VICTOR = 'Victor' #竞选成功的人


ctx = GetContext()
selfAddr = GetExecutingScriptHash()


def Main(operation, args):
    if operation == 'createVoteAction':
        if len(args) != 2:
            return False
        actionName = args[0]
        admin = args[1]
        return createVoteAction(actionName, admin)
    if operation == 'getVoteAction':
        if len(args) != 1:
            return False
        actionName = args[0]
        return getVoteAction(actionName)
    if operation == 'applyToCandidate':
        if len(args) != 2:
            return False
        actionName = args[0]
        address = args[1]
        return applyToCandidate(actionName, address)
    if operation == 'getApplyInfo':
        if len(args) != 1:
            return False
        actionName = args[0]
        return getApplyInfo(actionName)
    if operation == 'approveApply':
        if len(args) != 3:
            return False
        actionName = args[0]
        admin = args[1]
        address = args[2]
        return approveApply(actionName, admin, address)
    if operation == 'getCandadite':
        if len(args) != 1:
            return False
        actionName = args[0]
        return getCandadite(actionName)
    if operation == "vote":
        if len(args) != 3:
            return False
        actionName = args[0]
        voter = args[1]
        candidate = args[2]
        return vote(actionName, voter, candidate)
    if operation == "getPoll":
        actionName = args[0]
        candadite = args[1]
        return getPoll(actionName, candadite)
    if operation == "endAction":
        actionName = args[0]
        admin = args[1]
        return endAction(actionName, admin)
    if operation == "getVictor":
        actionName = args[0]
        return getVictor(actionName)



def createVoteAction(actionName, admin):
    '''
    create a vote action
    :return:
    '''
    if Get(ctx, concat(KEY_VOTE_ACTION, actionName)):
        Notify(["action name have existed"])
        return False
    if not CheckWitness(admin):
        Notify(["admin CheckWitness failed"])
        return False
    # 0表示投票进行中  1表示投票结束
    actionInfo = [actionName, admin, 0]
    info = Serialize(actionInfo)
    Put(ctx, concat(KEY_VOTE_ACTION, actionName), info)
    Notify(["create action success"])
    return True


def getVoteAction(actionName):
    '''
    query vote action
    :return:
    '''
    info = Get(ctx, concat(KEY_VOTE_ACTION, actionName))
    if info is None or info == "":
        return False
    return Deserialize(info)


def applyToCandidate(actionName, address):
    '''
    apply to be candidate of a vote action
    :return:
    '''
    if not CheckWitness(address):
        return False
    if not Get(ctx, concat(KEY_CANDIDATE_APPLY, actionName)):
        appliesList = []
    else:
        appliers = Get(ctx, concat(KEY_CANDIDATE_APPLY, actionName))
        appliesList = Deserialize(appliers)
    for addr in appliesList:
        if addr == address:
            return False
    appliesList.append(address)
    appliers = Serialize(appliesList)
    Put(ctx, concat(KEY_CANDIDATE_APPLY, actionName), appliers)
    return True



def getApplyInfo(actionName):
    '''
    query apllier information
    :return:
    '''
    appliers = Get(ctx, concat(KEY_CANDIDATE_APPLY, actionName))
    applierList = Deserialize(appliers)
    return applierList


def approveApply(actionName, admin, address):
    '''
    admin of a vote action approve one's apply
    :return:
    '''
    if not Get(ctx, concat(KEY_CANDIDATE_APPLY, actionName)):
        return False
    if not CheckWitness(admin):
        return False
    info = Get(ctx, concat(KEY_VOTE_ACTION, actionName))
    Notify(["11111111111"])
    actionInfo = Deserialize(info)
    Notify(["2222222222", actionInfo[1]])
    if actionInfo[1] != admin:
        return False
    Notify(["33333333333"])
    appliers = Get(ctx, concat(KEY_CANDIDATE_APPLY, actionName))
    Notify(["4444444", appliers])
    if appliers is None or appliers == "":
        return False
    applierList = Deserialize(appliers)
    hasApplier = False
    for applier in applierList:
        if applier == address:
            hasApplier = True
    if not hasApplier:
        return False
    candidate = Get(ctx, concat(KEY_CANDIDATE, actionName))
    if candidate is None or candidate == "":
        candidateList = []
    else:
        candidateList = Deserialize(candidate)
    candidateList.append(address)
    Put(ctx, concat(KEY_CANDIDATE, actionName), Serialize(candidateList))
    applierList2 = []
    for applier in applierList:
        if applier != address:
            applierList2.append(applier)
    Put(ctx, concat(KEY_CANDIDATE_APPLY, actionName), Serialize(applierList2))
    return True


def getCandadite(actionName):
    '''
    query candidate info
    :return:
    '''
    candidate = Get(ctx, concat(KEY_CANDIDATE, actionName))
    if candidate is None or candadite == "":
        return False
    candidateList = Deserialize(candidate)
    return candidateList


def vote(actionName, voter, candidate):
    '''
    vote to candidate
    :return:
    '''
    if not CheckWitness(voter):
        return False
    candidates = Get(ctx, concat(KEY_CANDIDATE, actionName))
    if candidates is None or candidates == "":
        return False
    candidateList = Deserialize(candidates)
    hasCandidate = False
    for candi in candidateList:
        if candi == candidate:
            hasCandidate = True
    if not hasCandidate:
        return False
    num = Get(ctx, concat(concat(KEY_POLL, actionName), candidate))
    if num is None or num == "":
        num = 0
    num = num + 1
    Notify(["111111111", num])
    Notify(["222222", actionName,candidate])
    Put(ctx, concat(concat(KEY_POLL, actionName), candidate), num)
    return True


def getPoll(actionName, candidate):
    '''
    query poll
    :return:
    '''
    Notify(["11111"])
    num = Get(ctx, concat(concat(KEY_POLL, actionName), candidate))
    Notify(["222222", num])
    Notify(["3333333", actionName,candidate])
    if num is None or num == "":
        return 0
    return num


def endAction(actionName, admin):
    if not CheckWitness(admin):
        return False
    info = Get(ctx, concat(KEY_VOTE_ACTION, actionName))
    if info is None or info == "":
        return False
    actionInfo = Deserialize(info)
    if actionInfo[1] != admin:
        return False
    candidates = Get(ctx, concat(KEY_CANDIDATE, actionName))
    if candidates is None or candidates == "":
        return False
    candidateList = Deserialize(candidates)
    victor = ""
    victorNum = 0
    for candidate in candidateList:
        num = Get(ctx, concat(concat(KEY_POLL, actionName), candidate))
        if num is None or num == "":
            n = 0
        else:
            n = num
        if n > victorNum:
            victorNum = n
            victor = candidate
    actionInfo = [actionName, admin, 1]
    # update action state
    Put(ctx, concat(KEY_VOTE_ACTION, actionName), Serialize(actionInfo))
    resList = []
    resList.append(victor)
    resList.append(victorNum)
    Put(ctx, concat(KEY_VICTOR, actionName), Serialize(resList))
    return True


def getVictor(actionName):
    victor = Get(ctx, concat(KEY_VICTOR, actionName))
    if victor is None or victor == "":
        return False
    else:
        return Deserialize(victor)
