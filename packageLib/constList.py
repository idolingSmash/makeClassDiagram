#!/usr/bin/python
# -*- coding: utf-8 -*-

taggedValueModelElement=[
	"1h,0,jude.profiles,%3C%3Fxml+version+%3D+%221.0%22+encoding+%3D+%22UTF-8%22+standalone+%3D+%22yes%22%3F%3E%0D%0A%3CumlProfiles%3E%0D%0A+%3CumlProfile%3E%0D%0A++%3Cname%3Ejude.profiles%3C%2Fname%3E%0D%0A+%3C%2FumlProfile%3E%0D%0A%3C%2FumlProfiles%3E%0D%0A%0D%0A",
	"be,0,jude.usericons,%3C%3Fxml+version+%3D+%221.0%22+encoding+%3D+%22UTF-8%22+standalone+%3D+%22yes%22%3F%3E%0D%0A%3CmmUserIcon%3E%0D%0A+%3CmmUserIconInfo%3E%0D%0A++%3Cname%3Ejude.usericons%3C%2Fname%3E%0D%0A+%3C%2FmmUserIconInfo%3E%0D%0A%3C%2FmmUserIcon%3E%0D%0A%0D%0A",
	"61,0,jude.profile.java,true",
	"69,0,jude.profile.java.stereotypes,class%2Cattribute%2Coperation%2Cenum%2Cenum_constant",
	"2r,0,jude.profile.java.stereotype.class,name%3DJava+Class%0D%0Atarget%3DClass%2CAssociationClass%2CInterface%2CEntity%2CBoundary%2CControl%2CActor%0D%0Avisibility%3Dfalse%0D%0Arequired%3Dtrue%0D%0Atags%3Dannotations%2Catmark_interface%2Cstrictfp%0D%0Alabel%3D",
	"l,0,jude.profile.java.stereotype.attribute,name%3DJava+Attribute%0D%0Atarget%3DAttribute%0D%0Avisibility%3Dfalse%0D%0Arequired%3Dtrue%0D%0Atags%3Dannotations%2Ctransient%2Cvolatile%0D%0Alabel%3D",
	"0,0,jude.profile.java.stereotype.operation,name%3DJava+Method%0D%0Atarget%3DMethod%0D%0Avisibility%3Dfalse%0D%0Arequired%3Dtrue%0D%0Atags%3Dannotations%2Csynchronized%2Cnative%2Cstrictfp%0D%0Alabel%3D",
	"30,0,jude.profile.java.stereotype.enum,name%3Denum%0D%0Atarget%3DClass%2CAssociationClass%2CInterface%2CEntity%2CBoundary%2CControl%2CActor%0D%0Avisibility%3Dtrue%0D%0Arequired%3Dfalse%0D%0Atags%3D%0D%0Alabel%3D%3C%3Cenum%3E%3E",
	"aw,0,jude.profile.java.stereotype.enum_constant,name%3Denum+constant%0D%0Atarget%3DAttribute%0D%0Avisibility%3Dtrue%0D%0Arequired%3Dfalse%0D%0Atags%3D%0D%0Alabel%3D%3C%3Cenum+constant%3E%3E",
	"60,0,jude.profile.java.tags,annotations%2Catmark_interface%2Csynchronized%2Cnative%2Ctransient%2Cvolatile%2Cstrictfp",
	"6f,0,jude.profile.java.tag.annotations,name%3Djude.java.annotations%0D%0Atarget%3DClass%2CAssociationClass%2CInterface%2CEntity%2CBoundary%2CControl%2CActor%2CAttribute%2CMethod%0D%0Astereotype%3DJava+Class%2CJava+Attribute%2CJava+Method%0D%0Adefaultvalue%3D%0D%0Adefinition%3D%0D%0Atype%3Dtext%0D%0Alabel%3Dannotations%0D%0Aomit%3Dtrue",
	"4e,0,jude.profile.java.tag.atmark_interface,name%3Djude.java.atmark_interface%0D%0Atarget%3DClass%2CAssociationClass%2CInterface%2CEntity%2CBoundary%2CControl%2CActor%0D%0Astereotype%3DJava+Class%0D%0Adefaultvalue%3Dfalse%0D%0Adefinition%3D%0D%0Atype%3Dboolean%0D%0Alabel%3D%40interface%0D%0Aomit%3Dtrue",
	"t,0,jude.profile.java.tag.synchronized,name%3Djude.java.synchronized%0D%0Atarget%3DMethod%0D%0Astereotype%3DJava+Method%0D%0Adefaultvalue%3Dfalse%0D%0Adefinition%3D%0D%0Atype%3Dboolean%0D%0Alabel%3Dsynchronized%0D%0Aomit%3Dtrue",
	"al,0,jude.profile.java.tag.native,name%3Djude.java.native%0D%0Atarget%3DMethod%0D%0Astereotype%3DJava+Method%0D%0Adefaultvalue%3Dfalse%0D%0Adefinition%3D%0D%0Atype%3Dboolean%0D%0Alabel%3Dnative%0D%0Aomit%3Dtrue",
	"b8,0,jude.profile.java.tag.transient,name%3Djude.java.transient%0D%0Atarget%3DAttribute%0D%0Astereotype%3DJava+Attribute%0D%0Adefaultvalue%3Dfalse%0D%0Adefinition%3D%0D%0Atype%3Dboolean%0D%0Alabel%3Dtransient%0D%0Aomit%3Dtrue",
	"9j,0,jude.profile.java.tag.volatile,name%3Djude.java.volatile%0D%0Atarget%3DAttribute%0D%0Astereotype%3DJava+Attribute%0D%0Adefaultvalue%3Dfalse%0D%0Adefinition%3D%0D%0Atype%3Dboolean%0D%0Alabel%3Dvolatile%0D%0Aomit%3Dtrue",
	"1d,0,jude.profile.java.tag.strictfp,name%3Djude.java.strictfp%0D%0Atarget%3DClass%2CAssociationClass%2CInterface%2CEntity%2CBoundary%2CControl%2CActor%2CMethod%0D%0Astereotype%3DJava+Class%2CJava+Method%0D%0Adefaultvalue%3Dfalse%0D%0Adefinition%3D%0D%0Atype%3Dboolean%0D%0Alabel%3Dstrictfp%0D%0Aomit%3Dtrue"
]
