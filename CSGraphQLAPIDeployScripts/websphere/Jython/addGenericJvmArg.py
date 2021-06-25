#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#addGenericJvmArgs: 
# Usage:  wsadmin -f addGenericJvmArgs.py mycell mynode myserver jvm_arg_key jvn_arg_key_val
#
# This script will parse the existing generic Jvm args on the cell/node/server for 
# the jvm_arg_key passed in (for example -Dxxx.xx.xxx, -Xxxx ). If this key is found, 
# remove the key before adding the new passed in jvm_arg_key_value. 
#
# Assune that all jvm_arg_key_value in Jvm args are separated by white space (using standard split)

mycell = sys.argv[0]
mynode = sys.argv[1]
server1= sys.argv[2]
jvm_arg_key = sys.argv[3]
jvm_arg_key_val = sys.argv[4]


server1 = AdminConfig.getid('/Cell:'+mycell+'/Node:'+mynode+'/Server:'+server1+'/')
print server1

jvm_id=AdminConfig.list('JavaVirtualMachine',server1)
print jvm_id

# there are 2 ways that an  environment variable can be set for the Java Virtual Machine
# https://www.ibm.com/support/pages/how-modify-generic-jvm-arguments-and-java-system-properties-was-server
# either via generic JVM arg or add a custom property.
# Since dev doc shows that adding is via the generic JVM arg way, code will follow this setting.
# 
current_arguments_str=AdminConfig.showAttribute(jvm_id,"genericJvmArguments")
print 'JVM pre  UPDATE = '
print  current_arguments_str

# Convert from str to array using split to easily look for existing and replace with new key
current_args_array = current_arguments_str.split () 

# build up a new resulting array, stripping out any element with this key
i = 0
new_args_array = []
for x in current_args_array:
	foundkey = x.find (jvm_arg_key)
	if (foundkey != -1):
		print ('\nFound key in the array: ' + jvm_arg_key + ' at index: ' + str (i))
	else:
		new_args_array.append (x )
	i = i + 1


print ('\nAdd new key: ' + jvm_arg_key_val)
new_args_array.append (jvm_arg_key_val)

#convert array to str before setting
new_args_str = ' '.join([str(elem) for elem in new_args_array])

#modify genericJvmArguments
print AdminConfig.modify(jvm_id,[['genericJvmArguments', new_args_str]])
AdminConfig.save()

current_arguments_str=AdminConfig.showAttribute(jvm_id,"genericJvmArguments")
print 'JVM post UPDATE = ' 
print current_arguments_str

