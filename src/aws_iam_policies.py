import boto3
from .params import CONFIG

IAM = boto3.client('iam', config=CONFIG)

class ExtractIamPolicies:
    def query_all_iam_users(self):
        paginator = IAM.get_paginator('list_users') # Criando um paginator para listar os usuários

        # Coletando os usuarios
        users = []
        for page in paginator.paginate():
            users.extend(page['Users'])

        return users

    def query_all_iam_groups(self):
        paginator = IAM.get_paginator('list_groups')

        groups = []
        for page in paginator.paginate():
            groups.extend(page['Groups'])

        return groups

    def query_iam_user_groups(self, user_names):
        groups = []

        for user_name in user_names:
            paginator = IAM.get_paginator('list_groups_for_user')
            for page in paginator.paginate(UserName=user_name):
                for group in page['Groups']:
                    groups.append({'UserName':user_name, 'GroupId':group['GroupId']})
        return groups

    def query_aim_all_policies(self):
        paginator = IAM.get_paginator('list_policies')

        policies = []
        for page in paginator.paginate():
            policies.extend(page['Policies'])

        return policies

    def query_iam_groups_policies(self, groups_names):
        policies=[]

        for group_name in groups_names:
            paginator = IAM.get_paginator('list_attached_group_policies')
            for page in paginator.paginate(GroupName=group_name):
                for policie in page['AttachedPolicies']:
                    policies.append({'GroupName':group_name, 'PolicyArn':policie['PolicyArn']})
        return policies

    def query_iam_policies_version(self, keys_values):
        cols = ['Arn', 'DefaultVersionId', 'AttachmentCount']
        csvFile = pd.read_csv(AWS_IAM_POLICIES, usecols=cols)
        csvFile = csvFile[csvFile['AttachmentCount'] > 0]
        docs = []

        for index, row in csvFile.iterrows():
            response = IAM.get_policy_version(
                PolicyArn=row['Arn'],
                VersionId=row['DefaultVersionId']
            )

            docs.append({
                'PolicyArn': row['Arn'],
                'DefaultVersionId': row['DefaultVersionId'],
                'PolicyDocument': response['PolicyVersion']['Document']
            })

        return docs

    def queryGroupPoliciesInLine(self):
        group_names = self.readCSVColumn('GroupName', AWS_IAM_ALL_GROUPS)
        policies=[]
        docs=[]

        for group_name in group_names:
            paginator = IAM.get_paginator('list_group_policies')
            for page in paginator.paginate(GroupName=group_name):
                if(len(page['PolicyNames'])>0):
                    policies.append({'GroupName':group_name, 'PolicyNames':page['PolicyNames']})

        for policy in policies:
            group_name = policy['GroupName']
            for policy_name in policy['PolicyNames']:
                response = IAM.get_group_policy(GroupName=group_name, PolicyName=policy_name)
                docs.append({
                    'GroupName':response['GroupName'],
                    'PolicyName':response['PolicyName'],
                    'PolicyDocument':response['PolicyDocument']
                })

        return docs

    def queryUserPoliciesInLine(self):
        user_names = self.readCSVColumn('UserName', AWS_IAM_ALL_USERS)
        policies=[]
        docs=[]

        for user_name in user_names:
            paginator = IAM.get_paginator('list_user_policies')
            for page in paginator.paginate(UserName=user_name):
                if(len(page['PolicyNames'])>0):
                    policies.append({'UserName':user_name, 'PolicyNames':page['PolicyNames']})

        for policy in policies:
            user_name = policy['UserName']
            for policy_name in policy['PolicyNames']:
                response = IAM.get_user_policy(UserName=user_name, PolicyName=policy_name)
                docs.append({
                    'UserName':response['UserName'],
                    'PolicyName':response['PolicyName'],
                    'PolicyDocument':response['PolicyDocument']
                })
        return docs
